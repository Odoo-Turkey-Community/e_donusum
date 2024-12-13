# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import api, fields, models
from odoo.exceptions import UserError

from odoo.addons.http_routing.models.ir_http import IrHttp
from markupsafe import Markup


class GibIncomingInvoice(models.Model):

    _name = "gib.incoming.invoice"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Gelen Fatura"
    _order = "issue_date DESC,id"

    name = fields.Char("Fatura No")
    ETTN = fields.Char("ETTN")
    issue_date = fields.Date("Fatura Tarihi")
    is_importable = fields.Boolean("İşlendi", default=False)

    sender = fields.Char("Faturayı Kesen")
    sender_vat = fields.Char("Vergi No")
    sender_alias = fields.Char("Gönderen PK")
    reciever_alias = fields.Char("Alıcı PK")

    invoice_type = fields.Char(string="Fatura Tipi")
    gib_profile = fields.Char(string="Fatura Türü")
    gib_provider_id = fields.Many2one(
        comodel_name="gib_base_2kb.provider", string="Entegratör", required=True
    )
    state = fields.Selection(
        selection=[
            ("Waiting", "Bekliyor"),
            ("Accepted", "Kabul Edildi"),
            ("Rejected", "Reddedildi"),
            ("Deny", "Aktarma"),
        ],
        string="Durumu",
    )

    currency_code = fields.Char("Para Birimi")
    tax_group = fields.Char("Vergi Grubu")
    tax_code = fields.Char("Vergi Kodu")
    tax_amount = fields.Float("Vergi Tutarı")
    tax_exclude = fields.Float("Vergi Hariç Tutar")
    total_amount = fields.Float("Vergi Dahil Tutar")
    is_approvable = fields.Boolean(compute="_compute_is_approvable", store=True)
    company_id = fields.Many2one(
        "res.company", related="gib_provider_id.company_id", store=True
    )

    @api.depends("gib_profile", "issue_date", "state")
    def _compute_is_approvable(self):
        for record in self.filtered(lambda inv: inv.issue_date):
            record.is_approvable = False
            if (
                record.gib_profile == "TICARIFATURA"
                and not record.state
                and ((fields.date.today() - record.issue_date).days < 15)
            ):
                record.is_approvable = True
        self.filtered(lambda inv: not inv.issue_date).is_approvable = True

    def approve_or_deny(self, answer=None, text=""):
        if not answer:
            answer = self.env.context.get("answer")

        success, error = self.gib_provider_id.approve_or_deny(self.ETTN, answer, text)
        if success:
            if answer == "KABUL":
                self.state = "Accepted"
                self.message_post(
                    body=Markup(
                        "<span style='color:limegreen'>Ticari Fatura Kabul Edildi.</span>"
                    ),
                )
            elif answer == "RED":
                self.state = "Rejected"
                self.message_post(
                    body=Markup(
                        "<span style='color:indianred'>Ticari Fatura Reddedildi.</span>"
                    ),
                )
        else:
            raise UserError(error)

    def get_incoming_e_inv_pdf(self):
        return {
            "type": "ir.actions.act_url",
            "name": "PDF - %s" % self.name,
            "target": "new",
            "url": "/gib_invoice_2kb/pdf/incoming/%s" % (IrHttp._slug(self),),
        }

    def toggle_is_importable(self):
        for rec in self:
            rec.is_importable = not rec.is_importable

    def get_incoming_invoice_detail(self):
        self.gib_provider_id.get_incoming_invoice_xml(self.ETTN)

        return True
