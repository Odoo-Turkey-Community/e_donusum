# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import api, models


class GibProvider(models.Model):

    _inherit = "gib_base_2kb.provider"

    @api.model
    def _get_incoming_invoices(self, erp_status, startDate, endDate):
        """
        Bu method providerların servislerden
        gelen faturaları almasını sağlar.
        Gelen fatura kullanmak isteyen her provider
        bu methodu inherit etmeli"""
        return []

    @api.model
    def _set_incoming_invoices_status(self, invoices, operation):
        return True

    @api.model
    def get_invoice_pdf(self, invoices):
        return True

    def approve_or_deny(self, ettn, answer, text):
        self.ensure_one()
        return True
