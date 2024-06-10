# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    tax_office_id = fields.Many2one(
        related="partner_id.tax_office_id",
        string="Tax Office",
        required=True,
        store=True,
        readonly=False,
        ondelete="restrict"
    )
