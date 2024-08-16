# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import api, fields, models
from odoo.exceptions import UserError

from markupsafe import Markup

class GibInvoiceRestrictedCancelWizard(models.TransientModel):

    _name = "gib.invoice.restricted.cancel.wizard"
    _description = "Harici iptal"

    name = fields.Char()
    invoice_id = fields.Many2one("account.move", string="İptal Edilecek Fatura")
    gib_invoice_name = fields.Char(related="invoice_id.gib_invoice_name")
    invoice_date = fields.Date(related="invoice_id.invoice_date")
    gib_status = fields.Many2one(related="invoice_id.gib_status_code_id")
    partner_id = fields.Many2one(
        related="invoice_id.partner_id", string="Fatura Kesilen"
    )
    cancel_reason = fields.Selection(
        selection=[
            ("esign", "GİB İptal Portali üzerinden Mali Mühür ile İptal"),
            ("noter", "Noter üzerinden resmi tebligat ile İptal"),
            ("ptt", "PTT İadeli Taahhütlü İle İptal"),
            ("kep", "Kep ile İptal"),
        ],
        string="İptal Sebebi",
        required=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res_id = self.env.context.get("active_id")
        res_model = self.env.context.get("active_model")
        if res_id and res_model:
            res.update({"invoice_id": self.env[res_model].browse(res_id).id})
        return res

    def force_to_cancel_gib_invoice(self, **kwargs):
        for wizard in self:
            if wizard.invoice_id.gib_profile_id in [
                False,
                self.env.ref("gib_invoice_2kb.profile_id-EARSIVFATURA"),
            ]:
                raise UserError(
                    "Bu fatura harici olarak iptal edilebilir durumda değil"
                )
            wizard.invoice_id._check_fiscalyear_lock_date()
            wizard.invoice_id.button_cancel()
            wizard.invoice_id.external_cancellation = wizard.cancel_reason
            message_body = f"""
                <p style="color:indianred">Fatura Harici Olarak İptal Edildi.</p>
                <ul class="o_mail_thread_message_tracking">
                    <li>
                        İptal Sebebi:
                        <span> {dict(self.env[wizard._name].fields_get(allfields=["cancel_reason"])["cancel_reason"]['selection'])[wizard.cancel_reason]} Edildi.</span>
                    </li>
                </ul>
            """

            wizard.invoice_id.message_post(
                body=Markup(message_body),
                subject=None,
                message_type="notification",
                subtype_id=None,
                parent_id=False,
                attachments=None,
                **kwargs,
            )
