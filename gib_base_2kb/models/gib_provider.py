# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import models, fields, api, Command
from odoo.tools import html_escape
from odoo.modules.module import get_module_resource
from odoo.tools.mimetypes import guess_mimetype

from lxml import etree
import base64
import logging

_logger = logging.getLogger(__name__)


class GibUBLProvider(models.Model):
    _name = "gib_base_2kb.provider"
    _description = "Gib Provider"
    _order = "sequence, id"

    name = fields.Char("Özel Entegratör", required=True)
    active = fields.Boolean(default=True)
    provider = fields.Selection(
        selection=[("none", "Entegratör Ayarlanmamış")],
        string="Entegratör",
        default="none",
        required=True,
    )
    sequence = fields.Integer(default=10)
    partner_id = fields.Many2one("res.partner", related="company_id.partner_id")
    company_id = fields.Many2one(
        "res.company",
        required=True,
        readonly=True,
        default=lambda self: self.env.company,
    )
    vat = fields.Char(related="company_id.partner_id.commercial_partner_id.vat")

    prod_environment = fields.Boolean(
        "Canlı Ortam", help="Canlı ortamda çalışmak için işaretleyin.", default=True
    )
    send_as_draft = fields.Boolean("Taslak Olarak Gönder", default=True)
    invoice_logo = fields.Image(
        "Döküman Logosu",
        max_width=128,
        max_height=128,
    )
    invoice_sign = fields.Image(
        "Döküman İmzası",
        max_width=128,
        max_height=128,
        help="E-arşiv için İmza görseli",
    )
    bank_ids = fields.One2many(
        help="Fatura çıktısında altta listelenecek bankalar",
        related="company_id.partner_id.commercial_partner_id.bank_ids",
        readonly=False,
    )
    conn_srv = fields.Char("Sunucu", default="https://api.kitayazilim.com.tr")
    conn_user = fields.Char("Kullanıcı Adı")
    conn_password = fields.Char("Şifre")

    def _save_template(self, template, template_name, profile_ids):
        result = []
        if "invoice_logo" in self and self.invoice_logo:
            content_type = guess_mimetype(base64.b64decode(self.invoice_logo))
            safe_types = ["image/jpeg", "image/png", "image/gif", "image/x-icon"]
            if content_type in safe_types:
                logo_node = template.xpath('//img[@id="company_logo"]')
                if len(logo_node):
                    logo_node[0].attrib["src"] = (
                        f"data:{content_type};base64,"
                        + self.invoice_logo.decode("utf8")
                    )

        if "invoice_sign" in self and self.invoice_sign:
            content_type = guess_mimetype(base64.b64decode(self.invoice_sign))
            safe_types = ["image/jpeg", "image/png", "image/gif", "image/x-icon"]
            if content_type in safe_types:
                logo_node = template.xpath('//img[@id="company_sign"]')
                if len(logo_node):
                    logo_node[0].attrib["src"] = (
                        f"data:{content_type};base64,"
                        + self.invoice_sign.decode("utf8")
                    )

        ir = self.env["ir.attachment"]
        einv_temp = ir.search([("name", "=", template_name)], limit=1)
        xml = etree.tostring(template, encoding="UTF-8")
        if einv_temp:
            einv_temp.write(
                {
                    "datas": base64.b64encode(xml),
                    "mimetype": "application/xslt+xml",
                    "name": template_name,
                    "use_for_electronic": True,
                }
            )
            if not einv_temp.gib_profile_id:
                einv_temp.write(
                    {
                        "gib_profile_id": [
                            Command.link(profile) for profile in profile_ids
                        ],
                    }
                )
            result.append("Şablonu düzenlendi!")
        else:
            ir.with_context({}).create(
                {
                    "name": template_name,
                    "datas": base64.b64encode(xml),
                    "type": "binary",
                    "mimetype": "application/xslt+xml",
                    "use_for_electronic": True,
                    "gib_profile_id": [
                        Command.link(profile) for profile in profile_ids
                    ],
                }
            )
            result.append("Şablonu oluşturuldu!")
        return result

    def configure_gib_template(self):

        result_text = []
        earchive_template = etree.parse(
            get_module_resource("gib_base_2kb", "data", "template", "e-Arsiv.xslt")
        )
        einvoice_template = etree.parse(
            get_module_resource("gib_base_2kb", "data", "template", "e-Fatura.xslt")
        )
        if earchive_template:
            profile_ids = [self.env.ref("gib_invoice_2kb.profile_id-EARSIVFATURA").id]
            self._save_template(earchive_template, "E-Arsiv Tasarım", profile_ids)

        if einvoice_template:
            profile_ids = [
                self.env.ref("gib_invoice_2kb.profile_id-TEMELFATURA").id,
                self.env.ref("gib_invoice_2kb.profile_id-TICARIFATURA").id,
            ]
            self._save_template(einvoice_template, "E-Fatura Tasarım", profile_ids)

        message = "<br/>".join(result_text)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Yapılandırma Tamamlandı!",
                "message": message,
                "type": "success",
                "sticky": False,
            },
        }

    def get_default_provider(self, company_id=None):
        company = company_id or self.env.company
        return self.search([('company_id', '=', company.id)], limit=1)

    @api.model
    def _get_applicability(self, doc_id):
        """Doküman için provider tarafında yapılacak aksiyonları döner"""

        return {}

    ####################################################
    # Export method to override based on EDI Format
    ####################################################
    def _get_ubl_tr12_builder(self):
        return self.env["gib.ubl.tr12"]

    ####################################################
    # Other helpers
    ####################################################

    @api.model
    def _format_error_message(self, error_title, errors):
        bullet_list_msg = "".join("<li>%s</li>" % html_escape(msg) for msg in errors)
        return "%s<ul>%s</ul>" % (error_title, bullet_list_msg)

    def _check_provider_configuration(self):
        """
        Entegratörün ayalarını kontrol eder. Hataları array olarak geri döner!
        :return: array of str
        """
        return []

    ####################################################
    # Partner API
    ####################################################
    def get_partner_alias(self):
        self.company_id.partner_id.get_partner_alias()

    def _get_partner_alias(self, partner, role="PK"):
        """Partnerin etiket bilgisini günceller. default alias atamasını yapar.
        Api başarılı ise true-false şeklinde döner

        """
        return False

    def configure_cron(self):
        return True
