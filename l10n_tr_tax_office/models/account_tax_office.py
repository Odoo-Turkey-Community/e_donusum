# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import models, fields


class AccountTaxOffice(models.Model):
    _name = "account.tax.office"
    _description = "Tax Office"
    _order = "state_id, code"

    _sql_constraints = [
        (
            "account_tax_office_code_uniq",
            "UNIQUE(code)",
            "Account Tax Office Code must be unique.",
        )
    ]

    name = fields.Char("Tax Office Name", required=True)
    code = fields.Char("Tax Office Code", size=6, required=True)
    state_id = fields.Many2one("res.country.state", "State", required=True, ondelete="restrict")
    active = fields.Boolean("Active", default=True)
