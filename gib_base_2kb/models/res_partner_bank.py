# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import fields, models


class ResPartnerBank(models.Model):

    _inherit = "res.partner.bank"

    kt_branch = fields.Char("Banka Şubesi")
