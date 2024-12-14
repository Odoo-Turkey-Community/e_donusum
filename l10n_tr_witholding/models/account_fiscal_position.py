# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import models, fields


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'
    _rec_names_search = ['name', 'exception_code']

    exception_code = fields.Char('Exception Code')
    exemption_rate = fields.Float('Exemption Rate', digits=(3, 2))
    invoice_type = fields.Selection([
        ('exception', 'Exception'),
        ('withholding', 'Withholding'),
        ('export_registered', 'Export Registered'),
    ], string="Invoice Type")

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, "%s - %s" % (rec.exception_code or '', rec.name)))
        return res
