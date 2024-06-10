# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    tax_office_id = fields.Many2one("account.tax.office", "Tax Office", ondelete="restrict")
