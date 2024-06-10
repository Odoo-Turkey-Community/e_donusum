# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import json
import base64
from lxml import etree
from werkzeug.exceptions import InternalServerError
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
from odoo.tools.misc import html_escape


class Controller(http.Controller):

    @http.route(
        '/gib_invoice_2kb/pdf2/<model("account.move"):move>', type="http", auth="user"
    )
    def gib_invoice_out_pdf_(self, move):
        try:
            gib_attachment = move._get_edi_attachment()
            if not gib_attachment:
                raise UserError("Ek bulunamadı")

            tree = etree.fromstring(
                base64.b64decode(gib_attachment.with_context(bin_size=False).datas)
            )
            ns = {
                "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
                "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            }
            r = tree.xpath(
                "//cac:AdditionalDocumentReference[cbc:DocumentType[text() ='XSLT']]//cbc:EmbeddedDocumentBinaryObject",
                namespaces=ns,
            )
            if len(r) != 1:
                f_xslt = (
                    "e-Arsiv.xslt"
                    if move.gib_profile_id
                    == request.env.ref("gib_invoice_2kb.profile_id-EARSIVFATURA")
                    else "e-Fatura.xslt"
                )
                xslt = etree.parse(
                    get_module_resource("gib_base_2kb", "data", "template", f_xslt)
                )
            else:
                xslt = etree.fromstring(base64.b64decode(r[0].text))

            transform = etree.XSLT(xslt)
            print(transform.error_log)
            newdom = transform(tree)
            content = request.env["ir.actions.report"]._run_wkhtmltopdf(
                [str(newdom)],
                specific_paperformat_args={
                    "data-report-margin-top": 8,
                    "data-report-header-spacing": 8,
                },
            )
            headers = [
                ("Content-Type", "application/pdf"),
                (
                    "Content-Disposition",
                    "attachment; filename=" + move.gib_invoice_name + ".pdf;",
                ),
            ]
            return request.make_response(content, headers=headers)
        except Exception as e:
            se = http.serialize_exception(e)
            error = {"code": 200, "message": "Odoo Server Error", "data": se}
            res = request.make_response(html_escape(json.dumps(error)))
            raise InternalServerError(response=res) from e
