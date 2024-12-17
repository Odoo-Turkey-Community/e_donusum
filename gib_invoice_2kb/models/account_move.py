# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import uuid
import base64
import re
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.addons.http_routing.models.ir_http import IrHttp

from lxml import etree
from markupsafe import Markup

GIB_INVOICE_DEFAULT_NAME = "TASLAK"


class AccountMove(models.Model):
    _inherit = "account.move"

    gib_state = fields.Selection(
        selection=[
            ("to_send", "Gönderilecek"),
            ("sent", "Gönderildi"),
            ("to_cancel", "İptal Edilecek"),
            ("cancelled", "İptal"),
        ],
        string="Entegratör Durumu",
        help="Faturanın entegratör ile ilgili durumu",
        copy=False,
        readonly=True,
        tracking=True,
    )
    gib_uuid = fields.Char(
        string="uuid", copy=False, readonly=True, index=True, tracking=True
    )
    gib_invoice_name = fields.Char(
        "Fatura No", store=True, readonly=True, copy=False, tracking=True
    )

    gib_error_message = fields.Html(
        string="GİB Hata Mesajı",
        readonly=True,
        copy=False,
    )

    gib_show_cancel_button = fields.Boolean(compute="_compute_gib_show_cancel_button")
    gib_show_pdf_button = fields.Boolean(compute="_compute_gib_show_pdf_button")
    gib_show_abandon_cancel_button = fields.Boolean(
        compute="_compute_edi_show_abandon_cancel_button"
    )
    gib_content = fields.Binary(compute="_compute_gib_content", compute_sudo=True)
    gib_attachment_id = fields.Many2one(
        comodel_name="ir.attachment",
        groups="base.group_system",
        copy=False,
    )
    partner_vat = fields.Char(related="partner_id.vat")
    gib_profile_id = fields.Many2one(
        comodel_name="gib_base_2kb.code",
        string="Fatura Senaryosu",
        domain="[('type', '=', 'profile_id'), ('value2', '=', partner_profile_type)]",
        compute="_compute_gib_profile_id",
        store=True,
        readonly=False,
    )
    gib_profile_id_value = fields.Char(related="gib_profile_id.value")
    gib_sequence_id = fields.Many2one(
        "ir.sequence",
        string="Fatura Seri",
        help="Bu alan e-Dökümanlarda takip edilebilecek sıra numarasını belirtir",
        domain="[('gib_profile_id', 'in', [gib_profile_id]), ('company_id', '=', company_id)]",
        compute="_compute_gib_sequence_id",
        store=True,
        readonly=False,
    )
    gib_invoice_type_id = fields.Many2one(
        comodel_name="gib_base_2kb.code",
        string="Fatura Tipi",
        domain="[('type', '=', 'type_code')]",
        compute="_compute_gib_invoice_type_id",
        store=True,
    )
    gib_provider_id = fields.Many2one(
        comodel_name="gib_base_2kb.provider",
        string="Entegratör",
        compute="_compute_gib_provider_id",
        store=True,
        readonly=False,
    )

    gib_alias_pk = fields.Many2one(
        "gib_base_2kb.alias",
        "Alıcı Etiket",
        domain="[('document_type', '=', 'invoice'), ('role', '=', 'PK'), ('vkn_tckn', '=', partner_vat)]",
        compute="_compute_gib_alias_pk",
        store=True,
        readonly=False,
    )

    gib_template_id = fields.Many2one(
        "ir.attachment",
        domain="[('mimetype', '=', 'application/xslt+xml'), ('gib_profile_id', '=', gib_profile_id), ('company_id', '=', company_id)]",
        compute="_compute_gib_template_id",
        string="Fatura Şablonu",
        store=True,
        readonly=False,
    )

    gib_status_code_id = fields.Many2one(
        "gib_base_2kb.code",
        "GİB Durumu",
        help="Faturanın GİB üzerinden entegratör aracılığı ile alınan GİB teki Durumu",
        domain="[('type', '=', 'gib_status_code')]",
        readonly=True,
        copy=False,
    )

    gib_status_code_id_value2 = fields.Char(
        string="GİB Durum Kodu", related="gib_status_code_id.value2"
    )

    gib_response_code = fields.Selection(
        selection=[("accept", "Kabul"), ("reject", "Red")],
        readonly=True,
        copy=False,
        string="Ticari Fatura Yanıtı",
    )

    gib_report_code = fields.Selection(
        selection=[
            ("wait", "Raporlanacak"),
            ("done", "Raporlandı"),
            ("cancel", "Raporlanmasın"),
        ],
        readonly=True,
        copy=False,
        string="e-Arşiv Rapor Durumu",
    )

    move_is_invoice = fields.Boolean(
        string="GIB Fatura", compute="_compute_move_is_invoice", store=True
    )
    external_cancellation = fields.Selection(
        selection=[
            ("esign", "GİB İptal Portali üzerinden Mali Mühür ile İptal"),
            ("noter", "Noter üzerinden resmi tebligat ile İptal"),
            ("ptt", "PTT İadeli Taahhütlü İle İptal"),
            ("kep", "Kep ile İptal"),
        ],
        string="Harici İptal Şekli",
        readonly=True,
    )
    external_refund_ref = fields.Char(
        string="İade Referansı",
        compute="_compute_external_refund_ref",
        inverse="_inverse_external_refund_ref",
        store=True,
        readonly=False,
    )

    partner_profile_type = fields.Char(compute="_compute_partner_profile_type")

    @api.depends("commercial_partner_id")
    def _compute_partner_profile_type(self):
        for rec in self:
            rec.partner_profile_type = (
                "e-inv" if rec.commercial_partner_id.is_e_inv else "e-arsv"
            )

    @api.depends("ref")
    def _compute_external_refund_ref(self):
        for record in self:
            record.external_refund_ref = ""
            if record.ref and record.move_type in ["in_invoice", "out_refund"]:
                record.external_refund_ref = record.ref.upper()

    @api.onchange("external_refund_ref")
    def _inverse_external_refund_ref(self):
        for record in self:
            record.external_refund_ref = (record.external_refund_ref or "").upper()
            record.gib_invoice_name = ""
            if record.external_refund_ref and record.move_type in [
                "in_invoice",
                "out_refund",
            ]:
                record.gib_invoice_name = record.external_refund_ref.upper()

    @api.depends("move_type", "gib_profile_id")
    def _compute_move_is_invoice(self):
        for record in self:
            record.move_is_invoice = record.gib_profile_id and record.move_type in (
                "out_invoice",
                "in_refund",
            )

    @api.depends("gib_profile_id", "partner_id", "move_is_invoice", "company_id")
    def _compute_gib_sequence_id(self):
        for record in self:
            if not record.move_is_invoice:
                record.gib_sequence_id = False
            else:
                record.gib_sequence_id = record.commercial_partner_id.sequence_id.id
                if (
                    record.gib_profile_id.id
                    not in record.gib_sequence_id.gib_profile_id.ids
                    or record.gib_sequence_id.company_id != record.company_id
                ):
                    suitable_sequences = record.gib_sequence_id.search(
                        [("gib_profile_id", "in", record.gib_profile_id.id), ('company_id', '=', record.company_id.id)]
                    )
                    if len(suitable_sequences) == 1:
                        record.gib_sequence_id = suitable_sequences[:1]
                    else:
                        record.gib_sequence_id = False

    @api.depends("gib_profile_id", "move_is_invoice", "partner_id", "company_id")
    def _compute_gib_template_id(self):
        for record in self:
            if not record.move_is_invoice:
                record.gib_template_id = False
            else:
                default_template = self.env["ir.attachment"].search(
                    [
                        ("mimetype", "=", "application/xslt+xml"),
                        ("gib_profile_id", "=", record.gib_profile_id.id),
                        ("company_id", "=", record.company_id.id),
                    ],
                    limit=1,
                    order="id DESC",
                )
                record.gib_template_id = default_template

    @api.depends("move_is_invoice", "partner_id", "gib_profile_id")
    def _compute_gib_alias_pk(self):
        for record in self:
            if not record.move_is_invoice or record.gib_profile_id == self.env.ref(
                "gib_invoice_2kb.profile_id-EARSIVFATURA", False
            ):
                record.gib_alias_pk = False
            else:
                record.gib_alias_pk = record.commercial_partner_id.alias_pk.id

    @api.depends("move_is_invoice", "gib_profile_id", "company_id")
    def _compute_gib_provider_id(self):
        for record in self:
            if not record.move_is_invoice or not record.gib_profile_id:
                record.gib_provider_id = False
            else:
                if not record.gib_provider_id or record.company_id != record.gib_provider_id.company_id:
                    record.gib_provider_id = (
                        record.gib_provider_id.get_default_provider(record.company_id).id
                    )

    @api.depends("move_type", "partner_id")
    def _compute_gib_profile_id(self):
        for record in self:
            if record.move_type not in ["out_invoice", "in_refund"]:
                record.gib_profile_id = False
            else:
                record.gib_profile_id = record.commercial_partner_id.profile_id.id

    @api.depends("move_is_invoice", "gib_provider_id")
    def _compute_gib_invoice_type_id(self):
        for record in self:
            if not record.move_is_invoice:
                record.gib_invoice_type_id = False
            else:
                if record.move_type == "out_invoice":
                    record.gib_invoice_type_id = self.env.ref(
                        "gib_invoice_2kb.type_code-SATIS", False
                    )
                else:
                    record.gib_invoice_type_id = self.env.ref(
                        "gib_invoice_2kb.type_code-IADE", False
                    )

    @api.depends("state", "gib_state")
    def _compute_gib_content(self):
        for move in self:
            res = b""
            if move.gib_state in ("to_send", "to_cancel", "sent"):
                provider = move._get_gib_provider()
                config_errors = move._check_move_configuration(move)
                if config_errors:
                    res = base64.b64encode("\n".join(config_errors).encode("UTF-8"))
                else:
                    move_applicability = provider._get_move_applicability(move)
                    if move_applicability and move_applicability.get("gib_content"):
                        res = base64.b64encode(move_applicability["gib_content"](move))
            move.gib_content = res

    @api.depends("gib_state", "state", "move_type")
    def _compute_gib_show_pdf_button(self):
        for move in self:
            move.gib_show_pdf_button = True
            provider = move._get_gib_provider()
            if (
                move.state != "posted"
                or not provider
                or move.move_type not in ("out_invoice", "in_refund")
            ):
                move.gib_show_pdf_button = False
                continue

    @api.depends("gib_state")
    def _compute_show_reset_to_draft_button(self):
        """
            Move dijital ise taslağa dönemez!
        :rtype: object
        """
        # OVERRIDE
        super()._compute_show_reset_to_draft_button()

        for move in self:
            provider = move._get_gib_provider()
            if provider and move.gib_state in ("sent", "to_cancel", "cancel"):
                move.show_reset_to_draft_button = False
                break

    @api.depends("gib_state")
    def _compute_gib_show_cancel_button(self):
        for move in self:
            if move.state != "posted":
                move.gib_show_cancel_button = False
                continue

            move.gib_show_cancel_button = False
            provider = move._get_gib_provider()
            move_applicability = provider and provider._get_move_applicability(move)
            if (
                provider
                and move.gib_state == "sent"
                and move_applicability
                and move_applicability.get("cancel")
            ):
                move.gib_show_cancel_button = True
                break

    def button_cancel_posted_moves(self):
        """Gönderilmiş e-doküman iptal işlemini başlatır."""

        for move in self:
            if not move.gib_show_cancel_button:
                raise UserError("Bu fatura iptal edilebilir durumda değil!")
            provider = move._get_gib_provider()
            move._check_fiscalyear_lock_date()

            move_applicability = provider and provider._get_move_applicability(move)
            if (
                provider
                and move.gib_state == "sent"
                and move_applicability
                and move_applicability.get("cancel")
            ):
                move.message_post(body=_("Fatura iptal isteği alındı."))
                move.write(
                    {
                        "gib_state": "to_cancel",
                        "gib_error_message": False,
                    }
                )
                move.button_process_gib_web_services()

    def button_cancel(self):
        # OVERRIDE
        # Set the electronic document to be canceled and cancel immediately for synchronous formats.
        res = super().button_cancel()
        self.filtered(lambda doc: doc.gib_state == "to_cancel").write(
            {
                "gib_state": "cancelled",
                "gib_error_message": False,
            }
        )
        return res

    def button_draft(self):
        # OVERRIDE
        for move in self:
            if move.gib_show_cancel_button:
                raise UserError(
                    _(
                        "GIB'e gönderilmiş bir elektronik belge olduğu için %s numaralı bu faturayı düzenleyemezsiniz."
                        "Bunun yerine 'GİB İptal Talebi' düğmesini kullanın."
                    )
                    % move.display_name
                )
            move.gib_state = False

        res = super().button_draft()
        return res

    def _post(self, soft=True):
        # OVERRIDE
        # Set the electronic document to be posted and post immediately for synchronous formats.
        posted = super()._post(soft=soft)

        for move in posted:
            provider = move._get_gib_provider()
            if provider:
                move_applicability = provider._get_move_applicability(move)
                if move_applicability:
                    # set move default data
                    move._set_default()
                    errors = move._check_move_configuration(move)
                    if errors:
                        raise UserError(
                            _("Hatalı Fatura Yapılandırmas(lar)ı:\n\n%s")
                            % "\n".join(errors)
                        )
                    move.sudo()._add_queue()
        return posted

    def _add_queue(self):
        self._get_edi_attachment().unlink()
        self.sudo().write(
            {
                "gib_state": "to_send",
                "gib_attachment_id": False,
            }
        )

    def button_gib_status(self):
        self.ensure_one()
        provider = self._get_gib_provider()
        if not provider:
            return

        move_applicability_func = provider._get_move_applicability(self).get(
            "update_state"
        )
        if move_applicability_func:
            res = move_applicability_func(self).get(self, {})
            if res.get("success"):
                self.write(
                    {
                        "gib_status_code_id": res["result"].get("gib_status_code_id"),
                        "gib_response_code": res["result"].get("gib_response_code_id"),
                    }
                )
                if "gtb_refno" in self._fields:
                    self.write(
                        {
                            "gtb_refno": res["result"].get("gtb_refno"),
                            "gtb_tescilno": res["result"].get("gtb_tescilno"),
                            "gtb_intac_tarihi": res["result"].get("gtb_intac_tarihi"),
                        }
                    )

    def _set_default(self):
        """Onaylanacak Digital Faturaya bazi değerleri ve ön tanımlı değerleri atar"""
        self.ensure_one()
        if self.move_type == "in_refund" and self.gib_profile_id == self.env.ref(
            "gib_invoice_2kb.profile_id-TICARIFATURA"
        ):
            self.gib_profile_id = self.env.ref("gib_invoice_2kb.profile_id-TEMELFATURA")

        if not self.gib_uuid:
            self.gib_uuid = str(uuid.uuid4())

        if not self.gib_invoice_name:
            self.gib_invoice_name = GIB_INVOICE_DEFAULT_NAME

    def _gib_rename_seq(self):
        """Faturaya Numara vermek ve bu no'yu UBL'de günceller"""
        attachment = self.sudo().gib_attachment_id
        if not attachment:
            raise UserError("UBL not found")

        self.gib_invoice_name = self.env["ir.sequence"].next_by_code(
            self.gib_sequence_id.code, sequence_date=self.invoice_date
        )
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
                self.gib_invoice_name
            )
            tree.insert(
                tree.index(copy_indicator_elements[0]), etree.fromstring(to_inject)
            )
        else:
            id_elements[0].text = self.gib_invoice_name

        new_xml = etree.tostring(tree, xml_declaration=True, encoding="UTF-8")
        attachment.sudo().write(
            {
                "datas": base64.b64encode(new_xml),
                "mimetype": "application/xml",
            }
        )

    ####################################################
    # Business operations
    ####################################################
    def action_export_xml(self):
        self.ensure_one()
        if not self.move_is_invoice:
            raise UserError("Yalnızca faturalar için UBL İndirilebilirsiniz")
        if not self.gib_show_pdf_button:
            raise UserError(
                "Bu Fatura UBL İndirilebilecek durumda değil. Fatura Elektronik fatura olmalı"
            )
        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/account.move/%s/gib_content/%s.xml?download=1"
            % (self.id, self.gib_invoice_name),
        }

    def action_export_pdf(self):
        self.ensure_one()
        if not self._get_edi_attachment():
            provider = self._get_gib_provider()
            move_applicability = provider and provider._get_move_applicability(self)
            if move_applicability and move_applicability.get("gib_content"):
                move_applicability["gib_content"](self)

        return {
            "type": "ir.actions.act_url",
            "name": "PDF - %s" % self.name,
            "target": "new",
            "url": "/gib_invoice_2kb/pdf2/%s" % (IrHttp._slug(self),),
        }

    def button_process_gib_web_services(self):
        self.action_process_gib_web_services(with_commit=False)

    def action_process_gib_web_services(self, with_commit=True):
        doc = self.filtered(lambda d: d.gib_state in ("to_send", "to_cancel"))
        doc.gib_provider_id._process_web_services(doc)

    def _retry_edi_documents_error_hook(self):
        attachment_to_unlink = self.env["ir.attachment"]
        for doc in self:
            if doc.gib_state == "to_send":
                attachment_to_unlink |= doc.gib_attachment_id
                doc.write({"gib_attachment_id": False})

            doc.write(
                {
                    "gib_status_code_id": False,
                    "gib_error_message": False,
                }
            )

        attachment_to_unlink.sudo().unlink()
        return True

    def action_retry_edi_documents_error(self):
        self._retry_edi_documents_error_hook()
        self.action_process_gib_web_services()

    ####################################################
    # Export Electronic Document
    ####################################################

    def _get_edi_attachment(self):
        return self.sudo().gib_attachment_id

    def _del_edi_attachment(self):
        return self.sudo().gib_attachment_id.unlink()

    def _get_gib_provider(self):
        return self.gib_provider_id

    @api.model
    def _check_required_fields(self, record, field_names, custom_warning_message=""):
        """
        This function check that a field exists on a record or dictionaries
        returns a generic error message if it's not the case or a custom one if specified
        """

        if not isinstance(field_names, list):
            field_names = [field_names]

        if not record:
            return custom_warning_message or _(
                "The element %s is required on %s.", record, ", ".join(field_names)
            )

        missing_fields = [
            field_name for field_name in field_names if not record[field_name]
        ]
        # field is present
        if not missing_fields:
            return

        # field is not present
        if custom_warning_message or isinstance(record, dict):
            return custom_warning_message or _(
                "The element %s is required on %s.", record, ", ".join(missing_fields)
            )

        display_field_names = record.fields_get(missing_fields)
        if len(missing_fields) == 1:
            display_field = f"'{display_field_names[missing_fields[0]]['string']}'"
            return _(
                "%s alan(lar)ı %s için zorunlu!", display_field, record.display_name
            )
        else:
            display_fields = ", ".join(
                f"'{display_field_names[x]['string']}'" for x in display_field_names
            )
            return _(
                "%s alan(lar)ından en az biri %s için zorunlu!",
                display_fields,
                record.display_name,
            )

    def _check_tax_suitability(self, line):

        forbidden_rates = ["8", "18"]

        for tax in line.tax_ids.filtered(lambda tax: tax.tax_group_id.code == "0015"):
            if str(int(tax.amount)) in forbidden_rates:
                return f"{tax.name} için %{int(tax.amount)}  oranı  %{', %'.join(forbidden_rates)}  oranlarından biri olamaz"

    def _check_move_configuration(self, move):
        """Checks the move and relevant records for potential error (missing data, etc).

        :param move:    The move to check.
        :returns:       A list of error messages.
        """
        error = []
        error.extend(move.gib_provider_id._check_provider_configuration())

        not move.gib_template_id and error.append(
            "Lütfen entegratör detayından şablonları yapılandırın!"
        )

        not move.gib_provider_id.alias_inv_gb and error.append(
            f"{move.gib_provider_id.name} için Gönderici Etiketi (GB) zorunlu!"
        )

        # ! Bir sequence de onaylanmış son faturadan daha eski tarihli fatura kesilemez
        invoice_sequence = move.gib_sequence_id

        invoice_date = move.invoice_date
        last_invoice = self.env["account.move"].search(
            [
                ("move_is_invoice", "=", True),
                ("gib_sequence_id", "=", invoice_sequence.id),
                ("gib_invoice_name", "not in", [GIB_INVOICE_DEFAULT_NAME, "", False]),
            ],
            order="invoice_date DESC",
            limit=1,
        )

        last_invoice and last_invoice.invoice_date and last_invoice.invoice_date > invoice_date and error.append(
            f"{invoice_sequence.name} serisinde Fatura kesmeyi denediğiniz {invoice_date.strftime('%d.%m.%Y')} tarihinden sonra kesilmiş en az bir fatura var!"
        )

        move.gib_profile_id.id not in invoice_sequence.gib_profile_id.ids and invoice_sequence and error.append(
            f"{invoice_sequence.name} serisi {move.gib_profile_id.name} için uygun değildir. Bu Seri ile {', '.join(invoice_sequence.gib_profile_id.mapped('name'))} kesebilirsiniz!"
        )

        move.invoice_date > fields.Date.today() and error.append(
            "Fatura tarihi bugünden ileri bir tarih olamaz!"
        )

        move.invoice_date.year < 2005 and error.append(
            "Fatura tarihi 2005 öncesi bir tarih olamaz!"
        )

        if move.gib_sequence_id:
            next_sequence_number = move.gib_sequence_id.get_next_char(
                move.gib_sequence_id._get_current_sequence().number_next
            )

            not re.search(
                "^[A-Z0-9]{3}20[0-9]{2}[0-9]{9}$", next_sequence_number or ""
            ) and error.append(
                "Geçersiz Fatura id elemanı değeri. Fatura id ABC2024123456789 formatında olmalı!"
            )

            if (
                move.gib_invoice_name
                and move.gib_invoice_name != GIB_INVOICE_DEFAULT_NAME
                and move.gib_invoice_name[:3] != next_sequence_number[:3]
            ):
                error.append(
                    "Fatura Seri No uyuşmazliği! Lüften Fatura No ile Fatura Seri bilgilerini kontrol ediniz!"
                )

        # region ----------------- Move Master Doğrulamaları -----------------
        # region #! ------------------ Move Master Supplier ve Customer Doğrulamaları ------------------
        supplier = move.company_id.partner_id.commercial_partner_id
        customer = (
            move.partner_id
            if move.partner_id.type == "invoice"
            else move.commercial_partner_id
        )
        supplier_error = self._check_required_fields(
            supplier, ["name", "vat", "street", "city", "state_id"]
        )
        supplier_error and error.append(supplier_error)

        customer_mandatory = ["name", "vat"]

        if not move._customer_vat_is_required(customer):
            customer_mandatory.remove("vat")

        customer_error = self._check_required_fields(
            move.commercial_partner_id, customer_mandatory
        )
        customer_error and error.append(customer_error)

        customer_error = self._check_required_fields(
            customer, ["street", "city", "state_id"]
        )
        customer_error and error.append(customer_error)

        if not error:
            supplier_vat = re.sub(r"\D+", "", supplier.vat or "").strip()
            if not len(supplier_vat) in [10, 11]:
                error.append(
                    f"{supplier.display_name} için 10 basamaklı Vergi No ya da 11 basamaklı T.C. Kimlik no olmalı!"
                )
            if "vat" in customer_mandatory:
                customer_vat = re.sub(r"\D+", "", customer.vat or "").strip()
                if not len(customer_vat) in [10, 11]:
                    error.append(
                        f"Ödeyici {move.commercial_partner_id}, için 10 basamaklı Vergi No ya da 11 basamaklı T.C. Kimlik no olmalı!"
                    )

        # endregion
        # region #! ------------------ Move Master GİB Profil ID Doğrulamaları ------------------
        req_fields = ["gib_provider_id", "gib_sequence_id", "gib_invoice_type_id"]
        if move.gib_profile_id == self.env.ref(
            "gib_invoice_2kb.profile_id-EARSIVFATURA"
        ):
            move.gib_alias_pk and error.append(
                "E-Arşiv faturasında Gönderici Posta Kutusu Olamaz!"
            )
        else:
            req_fields.extend(["gib_alias_pk", "gib_profile_id"])

        move_error = self._check_required_fields(move, req_fields)
        if move_error:
            error.append(move_error)

        if (
            move.gib_provider_id.prod_environment
            and "vat" in customer_mandatory
            and supplier.vat == customer.vat
        ):
            error.append("Alıcı ve Satıcının Vergi No'ları farklı olmalı!")

        customer.commercial_partner_id.is_e_inv and move.gib_profile_id.value2 == "e-arsv" and error.append(
            "E-Fatura mükellefine E-Arşiv faturası kesilemez!"
        )
        not customer.commercial_partner_id.is_e_inv and move.gib_profile_id.value2 == "e-inv" and error.append(
            "E-Fatura mükellefi olmayana E-Fatura kesilemez!"
        )
        move.move_type == "in_refund" and move.gib_profile_id == self.env.ref(
            "gib_invoice_2kb.profile_id-TICARIFATURA"
        ) and error.append("İade faturaları 'Ticari Fatura' olamaz!")
        # endregion
        # region #! ------------------ Move Master GİB Fatura Türü Doğrulamaları ------------------
        move.gib_invoice_type_id.value == "IADE" and move.gib_profile_id_value not in [
            "TEMELFATURA",
            "EARSIVFATURA",
        ] and error.append(
            "Fatura Türü İade iken Fatura Senaryosu sadece Temel Fatura veya E-Arşiv olabilir!"
        )
        # endregion
        # region #! ------------------ Move Master Fiscal Position Doğrulamaları ------------------
        move.fiscal_position_id.invoice_type == "exception" and move.fiscal_position_id.exception_code != 351 and move.gib_invoice_type_id.value != "ISTISNA" and error.append(
            "Fatura türü bu mali koşul için uygun değildir. Fatura türü istisna olmalıdır!"
        )

        move.fiscal_position_id.exception_code == 351 and move.gib_invoice_type_id.value != "SATIS" and error.append(
            "Fatura türü bu mali koşul için uygun değildir. Fatura türü satış olmalıdır!"
        )

        # endregion
        # endregion
        # region ----------------- Move Line Doğrulamaları -----------------
        move_lines = move.invoice_line_ids.filtered(
            lambda line: line.display_type not in ("line_note", "line_section")
        )
        for line in move_lines:
            line_error = self._check_required_fields(line, ["tax_ids"])
            if line.discount < 0:
                error.append(
                    f"GİB faturalarında negatif(sıfırdan küçük) indirim desteklenmemektedir.{line.display_name}"
                )

            if line_error:
                error.append(line_error)

            line_tax_error = self._check_tax_suitability(line)
            if line_tax_error:
                error.append(line_tax_error)

        # endregion
        return error

    def _customer_vat_is_required(self, customer):
        is_required = True
        if (
            self.gib_profile_id
            == self.env.ref("gib_invoice_2kb.profile_id-EARSIVFATURA")
            and customer.is_company
        ):
            is_required = False
        return is_required

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_to_send(self):
        if any(move.gib_state not in (False, "to_send") for move in self):
            raise UserError(_("Daha önce GİB'e gönderilen faturalar silinemez!"))

    def unlink(self):
        self._del_edi_attachment()
        return super().unlink()

    def cancel_rejected_invoice(self):
        self.ensure_one()
        if self.gib_response_code != "reject":
            raise UserError(
                "Yalnızca Reddedilmiş faturalar için bu işlemi yapabilirsiniz!"
            )
        self._check_fiscalyear_lock_date()
        self.button_cancel()

        message_body = """
            <p style="color:indianred">Fatura İptal Edildi.</p>
            <ul class="o_mail_thread_message_tracking">
                <li>
                    İptal Sebebi:
                    <span> Reddedilmiş Fatura.</span>
                </li>
            </ul>
        """

        self.message_post(
            body=Markup(message_body),
            subject=None,
            message_type="notification",
            subtype_id=None,
            parent_id=False,
            attachments=None,
        )

    def cancel_undelivered_invoice(self):
        self.ensure_one()
        if self.gib_status_code_id_value2 not in ["error"]:
            raise UserError(
                "Yalnızca GİB e iletilemeyen faturalar için bu işlemi yapabilirsiniz!"
            )
        self._check_fiscalyear_lock_date()
        self.button_cancel()

        message_body = f"""
            <p style="color:indianred">Fatura İptal Edildi.</p>
            <ul class="o_mail_thread_message_tracking">
                <li>
                    İptal Sebebi:
                    <span> Hata Özeti: {self.gib_status_code_id}.</span>
                </li>
            </ul>
        """

        self.message_post(
            body=Markup(message_body),
            subject=None,
            message_type="notification",
            subtype_id=None,
            parent_id=False,
            attachments=None,
        )

    def retry_to_send_undelivered_invoice(self):
        self.ensure_one()
        if self.gib_status_code_id_value2 not in ["error"]:
            raise UserError(
                "Bu işlemi yalnızca GİB e iletilemeyen faturalar için kullanabilirsiniz"
            )
        self.gib_uuid = str(uuid.uuid4())
        self.action_retry_edi_documents_error()
