# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import http
from odoo.http import request


class Controller(http.Controller):
    @http.route(
        '/gib_invoice_2kb/pdf/incoming/<model("gib.incoming.invoice"):in_invoice>',
        type="http",
        auth="user",
    )
    def get_incoming_pdf(self, in_invoice):
        try:
            pdf_res = in_invoice.gib_provider_id.get_invoice_pdf(in_invoice.ETTN)
            pdfhttpheaders = [
                ("Content-Type", "application/pdf"),
                ("Content-Length", len(pdf_res.content)),
            ]
            return request.make_response(pdf_res.content, headers=pdfhttpheaders)
        except Exception:
            text = "PDF alınamadı. Lütfen daha sonra tekrar deneyiniz!"
            texthttpheaders = [
                ("Content-Type", "text/plain"),
                ("Content-Length", len(text)),
            ]
            return request.make_response(text, headers=texthttpheaders)
