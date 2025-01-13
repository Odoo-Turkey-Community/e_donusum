# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import os
import base64
import logging
import requests
from datetime import timedelta
from collections import namedtuple
from odoo import fields, models, api, Command
from odoo.tools.misc import file_path
from textwrap import dedent

from .izibiz_service import IzibizService

e_arsiv_report_mapping = {
    "100": "wait",
    "105": "wait",
    "110": "wait",
    "120": "wait",
    "130": "done",
    "200": "cancel",
}

_logger = logging.getLogger(__name__)
CRON_DEPENDS = {"name", "active"}


class GibProvider(models.Model):

    _inherit = "gib_base_2kb.provider"

    provider = fields.Selection(
        selection_add=[("izibiz", "İZİBİZ Bilişim Teknolojileri")],
        ondelete={"izibiz": "set default"},
    )
    izibiz_username = fields.Char(string="Username")
    izibiz_password = fields.Char(string="Password")
    izibiz_jwt = fields.Char(string="Token")
    izibiz_keep_log = fields.Boolean("Servis Loglarını Sakla", default=False)
    izibiz_cron_ids = fields.Many2many("ir.cron", string="İzibiz Servisler")

    def _sync_cron(self):
        """Synchronise the related cron fields to reflect this alert"""
        for provider in self:
            for cron_id in provider.with_context(active_test=False).izibiz_cron_ids:
                cron_required = provider.active
                cron_id.active = cron_required

    def write(self, values):
        super().write(values)
        if not CRON_DEPENDS.isdisjoint(values):
            self._sync_cron()
        if self.izibiz_jwt and ('izibiz_username' in values or 'izibiz_password' in values):
            super().write({
                'izibiz_jwt': False
            })


    def unlink(self):
        crons = self.izibiz_cron_ids.sudo()
        server_actions = crons.ir_actions_server_id
        super().unlink()
        crons.unlink()
        server_actions.unlink()

    def _get_izibiz_service(self):
        return IzibizService(self)

    ####################################################
    # Config Helper
    ####################################################
    def _check_provider_configuration(self):
        res = super()._check_provider_configuration()
        if self.provider != "izibiz":
            return res

        error = []
        if not self.izibiz_username or not self.izibiz_password:
            error += [f"{self.name} yapılandırma bilgileri bulunamadı!"]
        return error

    def _check_picking_configuration(self):
        return self._check_provider_configuration()

    def dowload_wsdl(self):
        """Servis için gerekli olan WDSL dökümanları locale indirir"""
        modelu_path = file_path("izibiz_2kb")
        demo_link = {
            "auth": "https://efaturatest.izibiz.com.tr/AuthenticationWS?wsdl",
            "e-fatura": "https://efaturatest.izibiz.com.tr/EInvoiceWS?wsdl",
            "e-arsiv": "https://efaturatest.izibiz.com.tr/EIArchiveWS/EFaturaArchive?wsdl",
            "e-irs": "https://efaturatest.izibiz.com.tr/EIrsaliyeWS/EIrsaliye?wsdl",
        }
        for name, link in demo_link.items():
            request = requests.get(link, timeout=10)
            if request.status_code == 200:
                fpath = os.path.join(
                    modelu_path, "data", "wsdl", "demo", name + ".wsdl"
                )
                f_handle = open(fpath, "w")
                f_handle.write(request.text)
                f_handle.close()

        prod_link = {
            "auth": "https://authenticationws.izibiz.com.tr/AuthenticationWS?wsdl",
            "e-fatura": "https://efaturaws.izibiz.com.tr/EInvoiceWS?wsdl",
            "e-arsiv": "https://earsivws.izibiz.com.tr/EIArchiveWS/EFaturaArchive?wsdl",
            "e-irs": "https://eirsaliyews.izibiz.com.tr/EIrsaliyeWS/EIrsaliye?wsdl",
            # E-Müstahsil WS     https://emustahsilws.izibiz.com.tr/CreditNoteWS/CreditNote?wsdl
            # E-Mutabakat WS     https://emutabakatws.izibiz.com.tr/ReconciliationWS?wsdl
            # E-SMM WS           https://smmws.izibiz.com.tr/SmmWS?wsdl
        }
        for name, link in prod_link.items():
            request = requests.get(link, timeout=10)
            if request.status_code == 200:
                fpath = os.path.join(
                    modelu_path, "data", "wsdl", "prod", name + ".wsdl"
                )
                f_handle = open(fpath, "w")
                f_handle.write(request.text)
                f_handle.close()

    ####################################################
    # Partner API
    ####################################################

    def _get_partner_alias(self, vat, role="PK"):
        res = super()._get_partner_alias(vat, role)
        if self.provider != "izibiz":
            return res

        alias = []
        result = self._get_izibiz_service().check_user(vat, role)
        if result.get("error"):
            _logger.error("izibiz'den etiket alınamadı: " + result.get('error', ''))
        if result.get("success"):
            result_filter = [
                item for item in result.get("result") if item.DELETED == "N"
            ]
            for item in result_filter:
                alias.append(
                    {
                        "vkn_tckn": item.IDENTIFIER,
                        "title": item.TITLE,
                        "alias": item.ALIAS,
                        "type": item.TYPE,
                        "creationTime": fields.datetime.fromisoformat(
                            item.REGISTER_TIME
                        ),
                        "document_type": str(item.DOCUMENT_TYPE).lower(),
                        "role": item.UNIT,
                    }
                )

        return result.get("success"), alias

    ####################################################
    # Invoice API
    ####################################################

    def _move_post(self, moves):
        res = super()._move_post(moves)
        if self.provider != "izibiz":
            return res

        try:
            service = self._get_izibiz_service()
        except requests.exceptions.RequestException as e:
            for move in moves:
                res[move].update(
                    {
                        "success": False,
                        "blocking_level": "warning",
                        "error": "Entegratör cevap vermiyor! Lütfen daha sonra tekrar deneyiniz!\nHTTP Kodu: "
                        + str(e),
                    }
                )
            return res

        for move in moves:
            gb = (
                move.gib_provider_id.alias_inv_gb.alias
                if self.prod_environment
                else "urn:mail:defaultgb@izibiz.com.tr"
            )
            pk = (
                move.gib_alias_pk.alias
                if self.prod_environment
                else "urn:mail:defaultpk@izibiz.com.tr"
            )

            if move.gib_profile_id.value == "IHRACAT":
                pk = "urn:mail:ihracatpk@gtb.gov.tr"

            attachment = move._get_edi_attachment()
            data = base64.decodebytes(attachment.with_context(bin_size=False).datas)
            try:
                if move.gib_profile_id == self.env.ref(
                    "gib_invoice_2kb.profile_id-EARSIVFATURA"
                ):
                    sub_status = "DRAFT" if self.send_as_draft else "NEW"
                    result = service.write_to_archive_extended(
                        data, sub_status=sub_status
                    )
                else:
                    if not self.send_as_draft:
                        result = service.send_invoice(data, gb, pk)
                    else:
                        result = service.load_invoice(data)
            except requests.exceptions.RequestException as e:
                res[move].update(
                    {
                        "success": False,
                        "blocking_level": "warning",
                        "error": "Hata oluştu!\n" + str(e),
                    }
                )
                break
            res[move].update(result)

        return res

    def _move_update_state(self, moves):
        res = super()._move_update_state(moves)
        if self.provider != "izibiz":
            return res

        gib_status_code_ids = self.env["gib_base_2kb.code"].search(
            domain=[("type", "=", "gib_status_code")]
        )
        service = self._get_izibiz_service()
        for move in moves:
            is_e_arsiv = move.gib_profile_id == self.env.ref(
                "gib_invoice_2kb.profile_id-EARSIVFATURA"
            )
            move_info = res[move]
            try:
                if is_e_arsiv:
                    result = service.get_earchive_status(uuids=[move.gib_uuid])
                else:
                    result = service.get_invoice_status(uuid=move.gib_uuid)
            except requests.exceptions.RequestException as e:
                move_info.update(
                    {
                        "success": False,
                        "blocking_level": "warning",
                        "error": "Hata oluştu!\n" + str(e),
                    }
                )
                break

            if result.get("success"):
                move_info['success'] = True
                move_info['result'] = {}
                if is_e_arsiv:
                    gib_code = e_arsiv_report_mapping.get(
                        result["result"][0].HEADER.STATUS
                    )
                    move_info['result'].update(
                        {"gib_report_code": gib_code if gib_code else False}
                    )
                else:
                    move_info['result'].update(
                        {
                            "gib_status_code_id": fields.first(
                                gib_status_code_ids.filtered(
                                    lambda line: line.value
                                    == str(result["result"].GIB_STATUS_CODE)
                                )
                            ).id,
                            "gib_response_code": (
                                result["result"].RESPONSE_CODE in ["REJECT", "ACCEPT"]
                                and (
                                    "reject"
                                    if result["result"].RESPONSE_CODE == "REJECT"
                                    else "accept"
                                )
                                or False
                            ),
                            "gtb_refno": result["result"].GTB_REFNO,
                            "gtb_tescilno": result["result"].GTB_GCB_TESCILNO,
                            "gtb_intac_tarihi": result[
                                "result"
                            ].GTB_FIILI_IHRACAT_TARIHI,
                        }
                    )
        return res

    def _move_pdf(self, move):
        """
        return byte
        """
        res = super()._move_pdf(move)
        if self.provider != "izibiz":
            return res

        service = self._get_izibiz_service()
        if move.gib_profil_id == self.env.ref(
            "gib_invoice_2kb.profile_id-EARSIVFATURA"
        ):
            return service.read_from_archive(move.gib_uuid, format="PDF")
        else:
            return service.get_invoice_with_type(UUID=move.gib_uuid, TYPE="PDF")

    def _move_cancel(self, moves):
        res = super()._move_cancel(moves)
        if self.provider != "izibiz":
            return res

        service = self._get_izibiz_service()
        for move in moves:
            result = res[move]
            if move.gib_profile_id != self.env.ref(
                "gib_invoice_2kb.profile_id-EARSIVFATURA"
            ):
                result.update(
                    {
                        "success": False,
                        "blocking_level": "error",
                        "error": "Api üzerinden sadece e-Arşiv faturalar iptal edilebilir!",
                    }
                )
            else:
                try:
                    api = service.cancel_earchive_invoice(uuids=[move.gib_uuid])
                    result.update(api)
                except requests.exceptions.RequestException as e:
                    result.update(
                        {
                            "success": False,
                            "blocking_level": "warning",
                            "error": "Hata oluştu!\n" + str(e),
                        }
                    )
                    break

        return res

    ####################################################
    # İncoming e-İnvoice API
    ####################################################

    def _get_incoming_invoices(self, erp_status, startDate=False, endDate=False):
        res = super()._get_incoming_invoices(erp_status, startDate, endDate)
        if self.provider != "izibiz":
            return res

        state_mapping = {
            "REJECTED": "Rejected",
            "ACCEPTED": "Accepted",
        }
        service = self._get_izibiz_service()
        sdate = startDate.isoformat() if startDate else None
        edate = endDate.isoformat() if endDate else None
        read_included = False if not erp_status else True
        invoice_xmls = service.get_invoice(
            header_only="N",
            DIRECTION="IN",
            START_DATE=sdate,
            END_DATE=edate,
            READ_INCLUDED=read_included,
            LIMIT=100,
        )
        return [
            [
                invoice_xml.CONTENT._value_1.decode(),
                state_mapping.get(invoice_xml.HEADER.RESPONSE_CODE, "Waiting"),
            ]
            for invoice_xml in invoice_xmls["result"]
        ]

    def _set_incoming_invoices_status(self, invoices, operation):
        res = super()._set_incoming_invoices_status(invoices, operation)
        if self.provider != "izibiz":
            return res
        service = self._get_izibiz_service()
        service.mark_invoice(invoices)
        return True

    def get_invoice_pdf(self, invoice):
        res = super().get_invoice_pdf(invoice)
        if self.provider != "izibiz":
            return res
        service = self._get_izibiz_service()
        api = service.get_invoice_with_type(
            UUID=invoice, READ_INCLUDED="Y", TYPE="PDF", DIRECTION="IN", header_only="N"
        )
        PDF = namedtuple("PDF", ["content"])
        pdf = PDF(content=api["content"])
        return pdf

    def approve_or_deny(self, ettn, answer, text):
        res = super().approve_or_deny(ettn, answer, text)
        if self.provider != "izibiz":
            return res
        service = self._get_izibiz_service()
        api = service.send_invoice_response_with_server_sign(ettn, answer, text)
        return api["success"], api["error"]

    def _get_incoming_invoice_xml(self, ettn):
        res = super()._get_incoming_invoice_xml(ettn)
        if self.provider != "izibiz":
            return res

        service = self._get_izibiz_service()
        invoice_xmls = service.get_invoice(
            header_only="N",
            DIRECTION="IN",
            UUID=ettn,
            READ_INCLUDED=True,
            # LIMIT=100,
        )
        return invoice_xmls["success"], (
            invoice_xmls["result"][0].CONTENT._value_1
            if invoice_xmls["success"]
            else invoice_xmls["error"]
        )

    ####################################################
    # Cron Api
    ####################################################
    @api.model
    def _module_installed(self, name):
        return bool(
            self.env["ir.module.module"]
            .sudo()
            .search_count([("name", "=", name), ("state", "=", "installed")], limit=1)
        )

    def _configure_gib_user_list_change(self, cron_required):
        """ """
        cron_id = self.env.ref("izibiz_2kb.cron_get_gib_user_list", False)
        if cron_id:
            cron_id.write(
                {
                    "active": cron_required,
                    "code": dedent(
                        f"""\
                    # This cron is dynamically controlled by {self._description}.
                    # Do NOT modify this cron, modify the related record instead.
                    env['{self._name}'].browse([{self.id}]).cron_get_gib_user_list()"""
                    ),
                }
            )
        else:
            cron_id = (
                self.env["ir.cron"]
                .sudo()
                .create(
                    [
                        {
                            "user_id": self.env.ref("base.user_root").id,
                            "active": cron_required,
                            "interval_type": "days",
                            "interval_number": 1,
                            "numbercall": -1,
                            "doall": False,
                            "name": "izibiz_2kb: GIB etiket güncelle servisi  - %s"
                            % self.name,
                            "model_id": self.env["ir.model"]._get_id(self._name),
                            "state": "code",
                            "code": dedent(
                                f"""\
                # This cron is dynamically controlled by {self._description}.
                # Do NOT modify this cron, modify the related record instead.
                env['{self._name}'].browse([{self.id}]).cron_get_gib_user_list()"""
                            ),
                        }
                    ]
                )
            )
            self.env["ir.model.data"].create(
                {
                    "module": "izibiz_2kb",
                    "name": "cron_get_gib_user_list",
                    "model": "ir.cron",
                    "res_id": cron_id.id,
                    "noupdate": True,
                }
            )
        return cron_id

    def _configure_invoice_state(self, cron_required):
        cron_id = self.env.ref(
            "izibiz_2kb.cron_get_invoice_state_info_%d" % self.id, False
        )
        if cron_id:
            cron_id.write(
                {
                    "active": cron_required,
                }
            )
        else:
            cron_id = (
                self.env["ir.cron"]
                .sudo()
                .create(
                    [
                        {
                            "user_id": self.env.ref("base.user_root").id,
                            "active": cron_required,
                            "interval_type": "hours",
                            "interval_number": 4,
                            "numbercall": -1,
                            "doall": False,
                            "name": "izibiz_2kb: GIB Durum Kodları Güncelle - %s"
                            % self.name,
                            "model_id": self.env["ir.model"]._get_id(self._name),
                            "state": "code",
                            "code": dedent(
                                f"""\
                # This cron is dynamically controlled by {self._description}.
                # Do NOT modify this cron, modify the related record instead.
                env['{self._name}'].browse([{self.id}]).cron_get_invoice_state_info()"""
                            ),
                        }
                    ]
                )
            )
            self.env["ir.model.data"].create(
                {
                    "module": "izibiz_2kb",
                    "name": "cron_get_invoice_state_info_%d" % self.id,
                    "model": "ir.cron",
                    "res_id": cron_id.id,
                    "noupdate": True,
                }
            )
        return cron_id

    def _configure_invoice_responce(self, cron_required):
        cron_id = self.env.ref(
            "izibiz_2kb.cron_get_invoice_responce_info_%d" % self.id, False
        )
        if cron_id:
            cron_id.write(
                {
                    "active": cron_required,
                }
            )
        else:
            cron_id = (
                self.env["ir.cron"]
                .sudo()
                .create(
                    [
                        {
                            "user_id": self.env.ref("base.user_root").id,
                            "active": cron_required,
                            "interval_type": "hours",
                            "interval_number": 4,
                            "numbercall": -1,
                            "doall": False,
                            "name": "izibiz_2kb: GIB Ticari Cevap Servisi - %s"
                            % self.name,
                            "model_id": self.env["ir.model"]._get_id(self._name),
                            "state": "code",
                            "code": dedent(
                                f"""\
                # This cron is dynamically controlled by {self._description}.
                # Do NOT modify this cron, modify the related record instead.
                env['{self._name}'].browse([{self.id}]).cron_get_invoice_responce_info()"""
                            ),
                        }
                    ]
                )
            )
            self.env["ir.model.data"].create(
                {
                    "module": "izibiz_2kb",
                    "name": "cron_get_invoice_responce_info_%d" % self.id,
                    "model": "ir.cron",
                    "res_id": cron_id.id,
                    "noupdate": True,
                }
            )
        return cron_id

    def _configure_report_code(self, cron_required):
        cron_id = self.env.ref("izibiz_2kb.cron_get_report_code_%d" % self.id, False)
        if cron_id:
            cron_id.write(
                {
                    "active": cron_required,
                }
            )
        else:
            cron_id = (
                self.env["ir.cron"]
                .sudo()
                .create(
                    [
                        {
                            "user_id": self.env.ref("base.user_root").id,
                            "active": cron_required,
                            "interval_type": "hours",
                            "interval_number": 4,
                            "numbercall": -1,
                            "doall": False,
                            "name": "izibiz_2kb: GIB e-Arşiv Rapor Servisi - %s"
                            % self.name,
                            "model_id": self.env["ir.model"]._get_id(self._name),
                            "state": "code",
                            "code": dedent(
                                f"""\
                # This cron is dynamically controlled by {self._description}.
                # Do NOT modify this cron, modify the related record instead.
                env['{self._name}'].browse([{self.id}]).cron_get_report_code()"""
                            ),
                        }
                    ]
                )
            )
            self.env["ir.model.data"].create(
                {
                    "module": "izibiz_2kb",
                    "name": "cron_get_report_code_%d" % self.id,
                    "model": "ir.cron",
                    "res_id": cron_id.id,
                    "noupdate": True,
                }
            )
        return cron_id

    def _configure_export_invoice_info(self, cron_required):
        cron_id = self.env.ref(
            "izibiz_2kb.cron_get_export_invoice_info_%d" % self.id, False
        )
        if cron_id:
            cron_id.write(
                {
                    "active": cron_required,
                }
            )
        else:
            cron_id = (
                self.env["ir.cron"]
                .sudo()
                .create(
                    [
                        {
                            "user_id": self.env.ref("base.user_root").id,
                            "active": cron_required,
                            "interval_type": "hours",
                            "interval_number": 4,
                            "numbercall": -1,
                            "doall": False,
                            "name": "izibiz_2kb: GIB e-Ihracaat Bilgi Servisi - %s"
                            % self.name,
                            "model_id": self.env["ir.model"]._get_id(self._name),
                            "state": "code",
                            "code": dedent(
                                f"""\
                # This cron is dynamically controlled by {self._description}.
                # Do NOT modify this cron, modify the related record instead.
                env['{self._name}'].browse([{self.id}]).cron_get_export_invoice_info()"""
                            ),
                        }
                    ]
                )
            )
            self.env["ir.model.data"].create(
                {
                    "module": "izibiz_2kb",
                    "name": "cron_get_export_invoice_info_%d" % self.id,
                    "model": "ir.cron",
                    "res_id": cron_id.id,
                    "noupdate": True,
                }
            )
        return cron_id

    def _configure_despatch_state(self, cron_required):
        cron_id = self.env.ref(
            "izibiz_2kb.cron_daily_get_despatch_advice_%d" % self.id, False
        )
        if cron_id:
            cron_id.write(
                {
                    "active": cron_required,
                }
            )
        else:
            cron_id = (
                self.env["ir.cron"]
                .sudo()
                .create(
                    [
                        {
                            "user_id": self.env.ref("base.user_root").id,
                            "active": cron_required,
                            "interval_type": "hours",
                            "interval_number": 4,
                            "numbercall": -1,
                            "doall": False,
                            "name": "izibiz_2kb: GIB e-Irsaliye Bilgi Servisi - %s"
                            % self.name,
                            "model_id": self.env["ir.model"]._get_id(self._name),
                            "state": "code",
                            "code": dedent(
                                f"""\
                # This cron is dynamically controlled by {self._description}.
                # Do NOT modify this cron, modify the related record instead.
                env['{self._name}'].browse([{self.id}]).cron_daily_get_despatch_advice()"""
                            ),
                        }
                    ]
                )
            )
            self.env["ir.model.data"].create(
                {
                    "module": "izibiz_2kb",
                    "name": "cron_daily_get_despatch_advice_%d" % self.id,
                    "model": "ir.cron",
                    "res_id": cron_id.id,
                    "noupdate": True,
                }
            )
        return cron_id

    def _configure_income_invoice(self, cron_required):
        cron_id = self.env.ref(
            "izibiz_2kb.cron_daily_get_income_invoice_%d" % self.id, False
        )
        if cron_id:
            cron_id.write(
                {
                    "active": cron_required,
                }
            )
        else:
            cron_id = (
                self.env["ir.cron"]
                .sudo()
                .create(
                    [
                        {
                            "user_id": self.env.ref("base.user_root").id,
                            "active": cron_required,
                            "interval_type": "hours",
                            "interval_number": 4,
                            "numbercall": -1,
                            "doall": False,
                            "name": "izibiz_2kb: GIB Gelen e-Fatura Servisi - %s"
                            % self.name,
                            "model_id": self.env["ir.model"]._get_id(self._name),
                            "state": "code",
                            "code": dedent(
                                f"""\
                # This cron is dynamically controlled by {self._description}.
                # Do NOT modify this cron, modify the related record instead.
                env['{self._name}'].browse([{self.id}]).cron_daily_get_income_invoice()"""
                            ),
                        }
                    ]
                )
            )
            self.env["ir.model.data"].create(
                {
                    "module": "izibiz_2kb",
                    "name": "cron_daily_get_income_invoice_%d" % self.id,
                    "model": "ir.cron",
                    "res_id": cron_id.id,
                    "noupdate": True,
                }
            )
        return cron_id

    def configure_cron(self):
        res = super().configure_cron()
        if self.provider != "izibiz":
            return res

        # cron_get_gib_user_list
        cron_required = self.active
        cron_ids = []
        cron_id = self._configure_gib_user_list_change(cron_required)
        cron_ids.append(cron_id)

        cron_id = self._configure_invoice_state(cron_required)
        cron_ids.append(cron_id)

        cron_id = self._configure_invoice_responce(cron_required)
        cron_ids.append(cron_id)

        cron_id = self._configure_report_code(cron_required)
        cron_ids.append(cron_id)

        if self._module_installed("gib_invoice_pro_export_2kb"):
            cron_id = self._configure_export_invoice_info(cron_required)
            cron_ids.append(cron_id)

        if self._module_installed("gib_picking_2kb"):
            cron_id = self._configure_despatch_state(cron_required)
            cron_ids.append(cron_id)

        if self._module_installed("gib_incoming_invoice_2kb"):
            cron_id = self._configure_income_invoice(cron_required)
            cron_ids.append(cron_id)

        if cron_ids:
            self.izibiz_cron_ids = [Command.link(cron_id.id) for cron_id in cron_ids]

        return True

    # Cari
    def cron_get_gib_user_list(self, days_ago=3):
        service = self._get_izibiz_service()
        mdate = (fields.Date.today() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        result = service.get_gib_user_list(alias_modify_date=mdate)
        if not result["success"]:
            _logger.error("cron_get_gib_user_list: " + result["error"])
            return False

        identifier_list = set()
        for elem in result.get("result", []):
            identifier_list.add(elem.find("IDENTIFIER").text)

        partner_to_update = (
            self.env["res.partner"]
            .search([("vat", "in", list(identifier_list))])
            .commercial_partner_id
        )
        for partner in partner_to_update:
            partner.get_partner_alias()
        return True

    # region #! e-fatura, e-arşiv
    def cron_get_invoice_state_info(self, days_ago=7):
        "e-Fatura durum Güncelleme servisi"

        service = self._get_izibiz_service()
        sdate = (fields.Date.today() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        result = service.get_invoice(
            DIRECTION="OUT", START_DATE=sdate, DRAFT_FLAG="N", READ_INCLUDED="Y"
        )
        if not result["success"]:
            _logger.error("cron_get_invoice_state_info: " + result["error"])
            return False

        gib_status_code_ids = self.env["gib_base_2kb.code"].search_read(
            domain=[("type", "=", "gib_status_code")], fields=["id", "value"]
        )
        gib_status_code_map = {
            elem["value"]: elem["id"] for elem in gib_status_code_ids
        }

        api_state_map = {}
        for res in result["result"]:
            api_state_map[res.UUID] = str(res.HEADER.GIB_STATUS_CODE)

        move_state_map = {}
        move_ids = self.env["account.move"].search(
            [("gib_uuid", "in", list(api_state_map.keys()))]
        )
        for move_id in move_ids:
            move_state_map[move_id.gib_uuid] = (
                move_id.gib_status_code_id.value
                if move_id.gib_status_code_id.value
                else "-1"
            )
        state_sync_move = api_state_map.items() & move_state_map.items()
        state_sync_move_set = {s[0] for s in state_sync_move}
        filter_move_ids = move_ids.filtered(
            lambda move: move.gib_uuid not in state_sync_move_set
        )

        for move_id in filter_move_ids:
            status_id = gib_status_code_map.get(api_state_map[move_id.gib_uuid])
            if not status_id:
                code = api_state_map[move_id.gib_uuid]
                _logger.warning(
                    f"cron_get_invoice_state_info: Bilinmeyen durum kodu: {code} uuid: {move_id.gib_uuid}"
                )
            move_id.write({"gib_status_code_id": status_id})
        return True

    def cron_get_invoice_responce_info(self):
        """
        gib_response_code accept,reject değerlerini alabilir
        """
        gib_profile_id = self.env.ref("gib_invoice_2kb.profile_id-TICARIFATURA")
        domain = [
            ("gib_response_code", "=", False),
            ("gib_profile_id", "=", gib_profile_id.id),
            ("gib_provider_id.provider", "=", "izibiz"),
        ]
        move_ids = self.env["account.move"].search(domain, limit=1000)
        if not move_ids:
            return False

        service = self._get_izibiz_service()
        result = service.get_invoice_status_all(uuids=move_ids.mapped("gib_uuid"))

        if not result["success"]:
            _logger.error("cron_get_invoice_responce_info: " + result["error"])
            return False

        response_code_mapping = {
            "ACCEPTED": "accept",
            "REJECTED": "reject",
        }
        resp_mapping = {
            res.UUID: response_code_mapping.get(res.HEADER.RESPONSE_CODE)
            for res in result["result"]
        }
        for move_id in move_ids:
            if move_id.gib_uuid in resp_mapping:
                move_id.gib_response_code = resp_mapping.get(move_id.gib_uuid)

        return True

    def cron_get_report_code(self):
        """ """
        gib_profile_id = self.env.ref("gib_invoice_2kb.profile_id-EARSIVFATURA")
        domain = [
            ("gib_report_code", "=", False),
            ("gib_profile_id", "=", gib_profile_id.id),
            ("gib_provider_id.provider", "=", "izibiz"),
        ]
        move_ids = self.env["account.move"].search(domain, limit=1000)
        if not move_ids:
            return False

        service = self._get_izibiz_service()
        result = service.get_earchive_status(uuids=move_ids.mapped("gib_uuid"))

        if not result["success"]:
            _logger.error("cron_get_report_code: " + result["error"])
            return False

        resp_mapping = {
            res.HEADER.UUID: e_arsiv_report_mapping.get(res.HEADER.STATUS)
            for res in result["result"]
        }
        for move_id in move_ids:
            if move_id.gib_uuid in resp_mapping:
                move_id.gib_report_code = resp_mapping.get(move_id.gib_uuid)

        return True

    # TODO bu metho buradan kaldırılıp export modülüne taşınacak
    def cron_get_export_invoice_info(self):
        """
        gib_response_code accept,reject değerlerini alabilir
        """
        gib_profile_id = self.env.ref("gib_invoice_pro_export_2kb.profile_id-IHRACAT", False)
        domain = [
            ("gtb_refno", "=", False),
            ("gib_profile_id", "=", gib_profile_id.id),
            ("gib_provider_id.provider", "=", "izibiz"),
        ]
        move_ids = self.env["account.move"].search(domain, limit=1000)
        if not move_ids:
            return False

        service = self._get_izibiz_service()
        result = service.get_invoice_status_all(uuids=move_ids.mapped("gib_uuid"))

        if not result["success"]:
            _logger.error("cron_get_export_invoice_info: " + result["error"])
            return False

        resp_mapping = {
            res.UUID: {
                "gtb_refno": (res.HEADER.GTB_REFNO or "").strip() or False,
                "gtb_tescilno": res.HEADER.GTB_GCB_TESCILNO or False,
                "gtb_intac_tarihi": (
                    len(res.HEADER.GTB_FIILI_IHRACAT_TARIHI or "") == 10
                    and fields.date.fromisoformat(res.HEADER.GTB_FIILI_IHRACAT_TARIHI)
                )
                or False,
            }
            for res in result["result"]
        }
        for move_id in move_ids:
            if move_id.gib_uuid in resp_mapping:
                move_id.write(resp_mapping.get(move_id.gib_uuid))

        return True

    def cron_daily_get_income_invoice(self):
        """
        Günlük olarak gelen e-fatura'yı izibiz'den çeker.
        """
        ICP = self.env["ir.config_parameter"].sudo()
        GII = self.env["gib.incoming.invoice"].sudo()
        icp_key = f"izibiz.{self.name}.cron_daily_get_invoice_ldate_{self.id}"
        ldata_str = ICP.get_param(
            icp_key, (fields.Date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
        )
        response_code_mapping = {
            "ACCEPTED": "Accepted",
            "REJECTED": "Rejected",
        }

        service = self._get_izibiz_service()
        result = service.get_invoice(
            START_DATE=ldata_str, DIRECTION="IN", READ_INCLUDED="Y", DATE_TYPE="CREATE"
        )

        if not result["success"]:
            _logger.error("cron_daily_get_invoice_advice: " + str(result["error"]))
            return False

        _logger.info(
            "cron_daily_get_invoice_advice: Alınan fatura adedi: "
            + str(len(result["result"]))
        )
        gid_to_create = []
        for incoming in result["result"]:
            if incoming.HEADER.CDATE.strftime("%Y-%m-%d") > ldata_str:
                ldata_str = incoming.HEADER.CDATE.strftime("%Y-%m-%d")

            if GII.search([("ETTN", "=", incoming.UUID)]):
                continue

            gid_to_create.append(
                {
                    "gib_provider_id": self.id,
                    "ETTN": incoming.UUID,
                    "name": incoming.ID,
                    "gib_profile": incoming.HEADER.PROFILEID,
                    "invoice_type": incoming.HEADER.INVOICE_TYPE_CODE,
                    "reciever_alias": incoming.HEADER.TO,
                    "sender": incoming.HEADER.SUPPLIER,
                    "sender_vat": incoming.HEADER.SENDER,
                    "sender_alias": incoming.HEADER.FROM,
                    "issue_date": incoming.HEADER.ISSUE_DATE,
                    "total_amount": incoming.HEADER.PAYABLE_AMOUNT._value_1,
                    "currency_code": incoming.HEADER.PAYABLE_AMOUNT.currencyID,
                    "state": response_code_mapping.get(incoming.HEADER.RESPONSE_CODE),
                }
            )

        GII.create(gid_to_create)
        ICP.set_param(icp_key, ldata_str)
        _logger.info(
            "cron_daily_get_invoice_advice: Fatura alındı. Tarih: " + ldata_str
        )
        return True

    # endregion
    # region #! e-irsaliye
    def cron_daily_get_despatch_advice(self):
        """
        Günlük olarak gelen e-irsaliyeleri izibiz'den çeker.
        """
        ICP = self.env["ir.config_parameter"].sudo()
        GID = self.env["gib.incoming.despatch"].sudo()
        icp_key = f"izibiz.{self.name}.cron_daily_get_despatch_advice_ldate_{self.id}"
        ldata_str = ICP.get_param(
            icp_key, (fields.Date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
        )

        service = self._get_izibiz_service()
        result = service.get_despatch_advice(
            START_DATE=ldata_str, DIRECTION="IN", READ_INCLUDED="Y", DATE_TYPE="CREATE"
        )

        if not result["success"]:
            _logger.error("cron_daily_get_despatch_advice: " + result["error"])
            return False

        gid_to_create = []
        for incoming in result["result"]:
            if incoming.DESPATCHADVICEHEADER.CDATE.strftime("%Y-%m-%d") > ldata_str:
                ldata_str = incoming.DESPATCHADVICEHEADER.CDATE.strftime("%Y-%m-%d")

            if GID.search([("ETTN", "=", incoming.UUID)]):
                continue

            gid_to_create.append(
                {
                    "gib_provider_id": self.id,
                    "company_id": self.company_id.id,
                    "ETTN": incoming.UUID,
                    "name": incoming.ID,
                    "gib_profile": incoming.DESPATCHADVICEHEADER.PROFILEID,
                    "reciever": incoming.DESPATCHADVICEHEADER.RECEIVER
                    and incoming.DESPATCHADVICEHEADER.RECEIVER.ALIAS,
                    "reciever_vat": incoming.DESPATCHADVICEHEADER.RECEIVER
                    and incoming.DESPATCHADVICEHEADER.RECEIVER.VKN,
                    "sender": incoming.DESPATCHADVICEHEADER.SENDER
                    and incoming.DESPATCHADVICEHEADER.SENDER.ALIAS,
                    "sender_vat": incoming.DESPATCHADVICEHEADER.SENDER
                    and incoming.DESPATCHADVICEHEADER.SENDER.VKN,
                }
            )

        GID.create(gid_to_create)
        ICP.set_param(icp_key, ldata_str)
        return True

    # endregion
