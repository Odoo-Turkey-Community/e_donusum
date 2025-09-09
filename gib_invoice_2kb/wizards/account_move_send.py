# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import api, fields, models
from odoo.exceptions import UserError

from markupsafe import Markup


class AccountMoveSend(models.TransientModel):

    _inherit = "account.move.send"

    def _prepare_invoice_pdf_report(self, invoice, invoice_data):
        super()._prepare_invoice_pdf_report(invoice, invoice_data)
        if (
            invoice.gib_profile_id
            and invoice.gib_invoice_name
            and invoice.gib_state == "sent"
        ):
            content = invoice.get_2kb_pdf()
            invoice_data["pdf_attachment_values"].update({"raw": content})

    def _link_invoice_documents(self, invoice, invoice_data):
        if (
            not invoice.gib_profile_id
            or not invoice.gib_invoice_name
            or not invoice.gib_state == "sent"
        ):
            super()._link_invoice_documents(invoice, invoice_data)
            return

        invoice_sudo = invoice.sudo()
        attachment_name = f"{invoice_sudo.gib_invoice_name}_{invoice_sudo.gib_uuid}.pdf"
        attachment = invoice_sudo.attachment_ids.filtered(
            lambda atch: atch.name == attachment_name
        ).sorted(lambda r: r.create_date, reverse=True)
        attachment = attachment and attachment[-1] or False

        invoice_sudo.message_main_attachment_id = attachment.id
        invoice_sudo.invalidate_recordset(
            fnames=["invoice_pdf_report_id", "invoice_pdf_report_file"]
        )
        invoice_sudo.is_move_sent = True

    def _get_wizard_values(self):
        res = super()._get_wizard_values()
        res.update({"download": False})
        return res
