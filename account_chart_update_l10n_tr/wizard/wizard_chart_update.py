# Copyright 2024 Quanimo (https://www.quanimo.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class WizardUpdateChartsAccounts(models.TransientModel):
    _inherit = "wizard.update.charts.accounts"

    def _prepare_fp_vals(self, fp_template):
        val = super()._prepare_fp_vals(fp_template)
        val.update({
            'exception_code': fp_template.exception_code,
            'exemption_rate': fp_template.exemption_rate,
            'invoice_type': fp_template.invoice_type
        })
        return val
