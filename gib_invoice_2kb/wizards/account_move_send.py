# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from collections import defaultdict
from odoo import api, fields, models
from odoo.exceptions import UserError

from markupsafe import Markup


class AccountMoveSend(models.AbstractModel):

    _inherit = "account.move.send"

    def _prepare_invoice_pdf_report(self, invoices_data):
        invoices = self.env["account.move"].browse(
            [inv.id for inv in invoices_data.keys()]
        )
        run_super = invoices.filtered(
            lambda inv: not inv.gib_profile_id
            or not inv.gib_invoice_name
            or not inv.gib_state == "sent"
        )
        filtered_invoices_data = {
            inv: data for inv, data in invoices_data.items() if inv in run_super
        }
        if filtered_invoices_data:
            super()._prepare_invoice_pdf_report(invoices_data)

        filtered_invoices_data = {
            inv: data for inv, data in invoices_data.items() if inv not in run_super
        }
        for invoice, invoice_data in filtered_invoices_data.items():
            content = invoice.get_2kb_pdf()
            invoice_data["pdf_attachment_values"] = {
                "name": invoice._get_invoice_report_filename(),
                "raw": content,
                "mimetype": "application/pdf",
                "res_model": invoice._name,
                "res_id": invoice.id,
                "res_field": "invoice_pdf_report_file",  # Binary field
                "custom_pdf": True,
            }

    def _link_invoice_documents(self, invoice_data):

        super()._link_invoice_documents(
            {
                invoice: invoice_data
                for invoice, invoice_data in invoice_data.items()
                if not invoice_data.get("pdf_attachment_values", {}).get(
                    "custom_pdf", False
                )
            }
        )

        for invoice, invoice_data in invoice_data.items():
            if invoice_data.get("pdf_attachment_values", {}).get("custom_pdf", False):
                invoice_sudo = invoice.sudo()
                attachment_name = (
                    f"{invoice_sudo.gib_invoice_name}_{invoice_sudo.gib_uuid}.pdf"
                )
                attachment = invoice_sudo.attachment_ids.filtered(
                    lambda atch: atch.name == attachment_name
                ).sorted(lambda r: r.create_date, reverse=True)
                attachment = attachment and attachment[-1] or False

                invoice_sudo.message_main_attachment_id = attachment.id
                invoice_sudo.invalidate_recordset(
                    fnames=["invoice_pdf_report_id", "invoice_pdf_report_file"]
                )
                invoice_sudo.is_move_sent = True

    @api.model
    def _get_invoice_extra_attachments(self, move):
        if not move.gib_profile_id:
            return super()._get_invoice_extra_attachments(move)
        return move.attachment_ids.filtered(
            lambda atch: atch.name == f"{move.gib_invoice_name}_{move.gib_uuid}.pdf"
        )
