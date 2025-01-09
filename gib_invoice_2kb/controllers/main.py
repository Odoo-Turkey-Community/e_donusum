# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import json
from werkzeug.exceptions import InternalServerError
from odoo import http
from odoo.http import request
from odoo.tools.misc import html_escape


class Controller(http.Controller):

    @http.route(
        '/gib_invoice_2kb/pdf2/<model("account.move"):move>', type="http", auth="user"
    )
    def gib_invoice_out_pdf_(self, move):
        try:
            content = move.get_2kb_pdf()
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