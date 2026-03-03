# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class Controller(http.Controller):
    @http.route(
        '/gib_invoice_2kb/pdf/incoming/<model("gib.incoming.invoice"):in_invoice>',
        type="http",
        auth="user",
    )
    def get_incoming_pdf(self, in_invoice):
        # Todo Gelen fatura xml i kayıtta daha önce alınmışsa kayıtlı pdf i döndür, alınmamışsa entegratörün pdf alma servisinden alıp döndür
        try:
            pdf_res = in_invoice.gib_provider_id.get_invoice_pdf(in_invoice.ETTN)
            pdfhttpheaders = [
                ("Content-Type", "application/pdf"),
                ("Content-Length", len(pdf_res.content)),
            ]
            return request.make_response(pdf_res.content, headers=pdfhttpheaders)
        except Exception as e:
            _logger.error(
                "Gelen fatura PDF alınırken hata oluştu! ETTN: %s, Hata: %s",
                in_invoice.ETTN,
                e,
            )
            text = "PDF alınamadı. Lütfen daha sonra tekrar deneyiniz!"
            texthttpheaders = [
                ("Content-Type", "text/plain"),
                ("Content-Length", len(text)),
            ]
            return request.make_response(text, headers=texthttpheaders)
