# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import models, fields


class AccountFiscalPositionTemplate(models.Model):
    _inherit = 'account.fiscal.position.template'
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


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def _get_fp_vals(self, company, position):
        val = super()._get_fp_vals(company, position)
        val.update({
            'exception_code': position.exception_code,
            'exemption_rate': position.exemption_rate,
            'invoice_type': position.invoice_type
        })
        return val
