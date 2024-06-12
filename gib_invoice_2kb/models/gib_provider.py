# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import base64
import logging
import re
from lxml import etree


from odoo import models, api, fields
from odoo.exceptions import UserError
from .account_move import GIB_INVOICE_DEFAULT_NAME

_logger = logging.getLogger(__name__)


class GibUBLProvider(models.Model):
    _inherit = "gib_base_2kb.provider"

    alias_inv_gb = fields.Many2one(
        "gib_base_2kb.alias",
        string="Fat. Gönd. Birimi",
        domain="[('role', '=', 'GB'),('document_type','=','invoice'),('vkn_tckn', '=', vat)]",
    )

    def _get_applicability(self, doc_id):
        if doc_id._name != "account.move":
            return super()._get_applicability(doc_id)

        return self._get_move_applicability(doc_id)

    def _get_move_applicability(self, move):
        self.ensure_one()
        if (
            not move.is_invoice(include_receipts=True)
            or not move.gib_profile_id
            or move.move_type not in ("out_invoice", "in_refund")
            or move.country_code != "TR"
            or move.state != "posted"
        ):
            return {}

        invoice_type = move.gib_profile_id
        if invoice_type == self.env.ref("gib_invoice_2kb.profile_id-EARSIVFATURA"):
            return {
                "gib_content": self.gib_invoice_content,
                "post": self._move_post,
                "cancel": self._move_cancel,
                "update_state": self._move_update_state,
            }

        else:
            return {
                "gib_content": self.gib_invoice_content,
                "post": self._move_post,
                "update_state": self._move_update_state,
            }

    def gib_invoice_content(self, invoice):
        attachment = invoice._get_edi_attachment()
        if attachment:
            res = base64.decodebytes(attachment.with_context(bin_size=False).datas)
        else:
            builder = self._get_ubl_tr12_builder()
            res, _ = builder._export_invoice(invoice)
            attachment_create_vals = {
                "name": builder._export_invoice_filename(invoice),
                "raw": res,
                "mimetype": "application/xml",
            }
            invoice.sudo().write(
                {
                    "gib_attachment_id": self.env["ir.attachment"].create(
                        attachment_create_vals
                    )
                }
            )
        return res

    ####################################################
    # Invoice API
    ####################################################
    def _process_web_services(self, move):
        move.ensure_one()
        if move.gib_state == "to_send":
            result = self._move_post(move)[move]

            if result.get("success") is True:
                move.write({"gib_state": "sent", "gib_error_message": False})
            else:
                move.write({"gib_error_message": result.get("error", False)})
        elif move.gib_state == "to_cancel":
            result = self._move_cancel(move)[move]
            if result.get("success") is True:
                move.write(
                    {
                        "gib_state": "cancelled",
                        "gib_error_message": False,
                    }
                )
                move.button_cancel()
            else:
                move.write({"gib_error_message": result.get("error", False)})

    @api.model
    def _gib_rename_seq(self, move):
        """Faturaya Numara vermek ve bu no'yu UBL'de günceller"""

        move.gib_invoice_name = move.gib_sequence_id.next_by_id(
            sequence_date=move.invoice_date
        )

        if not re.search(
            "^[A-Z0-9]{3}20[0-9]{2}[0-9]{9}$", move.gib_invoice_name or ""
        ):
            raise UserError(
                "Geçersiz Fatura id elemanı değeri. Fatura id ABC2009123456789 formatında olmalıdır"
            )

    @api.model
    def _rename_update_ubl(self, move):
        attachment = move.sudo().gib_attachment_id
        old_xml = base64.b64decode(
            attachment.with_context(bin_size=False).datas, validate=True
        )

        tree = etree.fromstring(old_xml)
        nsmap = {k: v for k, v in tree.nsmap.items() if k is not None}
        id_elements = tree.xpath("/*/cbc:ID", namespaces=nsmap)
        copy_indicator_elements = tree.xpath("//*[local-name()='CopyIndicator']")
        if not id_elements:
            to_inject = """
                <cbc:ID xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2">%s</cbc:ID>
            """ % (
                move.gib_invoice_name
            )
            tree.insert(
                tree.index(copy_indicator_elements[0]), etree.fromstring(to_inject)
            )
        else:
            id_elements[0].text = move.gib_invoice_name

        new_xml = etree.tostring(tree, xml_declaration=True, encoding="UTF-8")
        attachment.sudo().write(
            {
                "datas": base64.b64encode(new_xml),
                "mimetype": "application/xml",
            }
        )

    def _move_pdf(self, move):
        """Belgeye ait PDF dosyasını indirmek için bu ucu kullanılır.

        :rtype: pdf content
        """
        self.ensure_one()
        return b""

    def _move_sign_ubl(self, moves):
        """Faturanın imzali UBL'lini döner.

        :rtype: dict
        """
        result = {}
        for move in moves:
            result.update({move: {}})
        return result

    def _move_post(self, moves):
        """Faturayi Entegratöre iletir.
        :rtype: Dict
        """
        # TODO  fatura no'da  kontrolu ve hata kontrolu yapıalacak
        cache_validate = False
        result = {}
        for move in moves:
            result = {move: {}}
            attachment = move._get_edi_attachment()
            if not attachment:
                if move.gib_invoice_name == GIB_INVOICE_DEFAULT_NAME:
                    try:
                        self._gib_rename_seq(move)
                    except UserError as e:
                        result[move].update(
                            {"blocking_level": "error", "error": str(e)}
                        )
                        continue
                self.gib_invoice_content(move)
            elif move.gib_invoice_name == GIB_INVOICE_DEFAULT_NAME:
                try:
                    self._gib_rename_seq(move)
                except UserError as e:
                    result[move].update({"blocking_level": "error", "error": str(e)})
                    continue
                self._rename_update_ubl(move)
                cache_validate = cache_validate or True

        if cache_validate:
            self.env.invalidate_all()

        return result

    def _move_cancel(self, moves):
        """Faturayi Entegratöre iletir.

        :rtype: dict
        """
        result = {}
        for move in moves:
            result.update({move: {}})
        return result

    def _move_update_state(self, moves):
        """Faturayi Entegratöre iletir.

        :rtype: dict content
        """
        result = {}
        for move in moves:
            result.update({move: {}})
        return result
