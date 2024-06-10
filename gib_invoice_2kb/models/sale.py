# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        # partner = self.env["res.partner"].browse(invoice_vals["partner_id"])
        # invoice_vals["gib_profile_id"] = partner.commercial_partner_id.profile_id.id
        return invoice_vals
