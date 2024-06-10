# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import models, fields


class Bank(models.Model):
    _inherit = 'res.bank'

    eft_code = fields.Char('EFT Code')
    website = fields.Char('Website Link')
