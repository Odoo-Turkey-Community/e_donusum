# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import requests
import copy

from odoo import api
from odoo.models import AbstractModel


class PublisherWarrantyContract(AbstractModel):
    _inherit = "publisher_warranty.contract"

    @api.model
    def _get_sys_logs(self):
        res = super()._get_sys_logs()

        try:
            msg = self._get_message()
            companies = self.env["res.company"].search([])
            vals = []
            for company in companies:
                new_msg = copy.deepcopy(msg)
                new_msg.update(
                    {
                        "auth_key_2kb": company.auth_key_2kb,
                        "vat": company.vat,
                        "company_id": company.id,
                    }
                )
                vals.append(new_msg)

            ICP = self.env["ir.config_parameter"].sudo().get_param
            url = ICP("2kb.base_url", "https://api.2kb.com.tr")
            url = url + "/publisher-warranty"

            payload = {"json_rpc": "2.0", "method": "POST", "params": {"vals": vals}}
            headers = {
                "Content-Type": "application/json",
            }
            requests.post(url, json=payload, headers=headers, timeout=30)
        except Exception:
            pass

        return res
