# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import _, api, fields, models

from markupsafe import Markup

class GibInvoiceArchiveCancelWizard(models.TransientModel):

    _name = "gib.invoice.archive.cancel.wizard"
    _description = "Harici iptal"

    name = fields.Char()
    invoice_id = fields.Many2one("account.move", string="İptal Edilecek Fatura")
    gib_invoice_name = fields.Char(related="invoice_id.gib_invoice_name")
    invoice_date = fields.Date(related="invoice_id.invoice_date")
    gib_status = fields.Many2one(related="invoice_id.gib_status_code_id")
    partner_id = fields.Many2one(
        related="invoice_id.partner_id", string="Fatura Kesilen"
    )
    cancel_reason = fields.Char(
        string="İptal Sebebi",
        required=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res_id = self.env.context.get("active_id")
        res_model = self.env.context.get("active_model")
        if res_id and res_model:
            invoice = self.env[res_model].browse(res_id)
            res.update({"invoice_id": invoice.id})
        return res

    def force_to_cancel_archive_invoice(self, **kwargs):
        for wizard in self:
            wizard.invoice_id.button_cancel_posted_moves()
            message_body = f"""
                <p style="color:indianred">E-Arşiv Fatura İptal Edildi.</p>
                <ul class="o_mail_thread_message_tracking">
                    <li>
                        İptal Sebebi:
                        <span>{wizard.cancel_reason}</span>
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
