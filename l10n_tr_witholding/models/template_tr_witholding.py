# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import models, _
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_chart_template_data(self, template_code):
        data = super()._get_chart_template_data(template_code)
        if template_code in ['tr', 'tr_witholding']:
            if 'template_data' in data:
                data['template_data'].update({'code_digits': '9'})
        return data

    @template('tr_witholding')
    def _get_tr_witholding_template_data(self):
        return {
            'name': _('Turkey Tax Witholding - 2KB Team)'),
            'parent': 'tr',
            'code_digits': '9',
            'property_account_receivable_id': 'tr120',
            'property_account_payable_id': 'tr320',
            'property_account_expense_categ_id': 'tr150',
            'property_account_income_categ_id': 'tr600',
        }

    @template('tr_witholding', 'res.company')
    def _get_tr_witholding_res_company(self):
        return {
            self.env.company.id: {
                'account_fiscal_country_id': 'base.tr',
                'bank_account_code_prefix': '102',
                'cash_account_code_prefix': '100',
                'transfer_account_code_prefix': '103',
                'account_default_pos_receivable_account_id': 'tr123',
                'income_currency_exchange_account_id': 'tr646',
                'expense_currency_exchange_account_id': 'tr656',
                'account_journal_suspense_account_id': 'tr102999',
                'account_journal_payment_debit_account_id': 'tr102997',
                'account_journal_payment_credit_account_id': 'tr102998',
                'account_sale_tax_id': 'tr_kdv_sale_20',
                'account_purchase_tax_id': 'tr_kdv_purchase_20'
            },
        }

    @template('tr_witholding', 'account.account')
    def _get_tr_witholding_account_account(self):
        tr_val = self._parse_csv('tr', 'account.account', module='l10n_tr')
        tr_ex_val = self._parse_csv('tr_witholding', 'account.account', module='l10n_tr_witholding')
        return {**tr_val, **tr_ex_val}

    @template('tr_witholding', 'account.tax.group')
    def _get_tr_witholding_account_tax_group(self):
        return self._parse_csv('tr_witholding', 'account.tax.group', module='l10n_tr_witholding')

    @template('tr_witholding', 'account.tax')
    def _get_tr_witholding_account_tax(self):
        return self._parse_csv('tr_witholding', 'account.tax', module='l10n_tr_witholding')

    @template('tr_witholding', 'account.fiscal.position')
    def _get_tr_witholding_account_fiscal_position(self):
        return self._parse_csv('tr_witholding', 'account.fiscal.position', module='l10n_tr_witholding')
