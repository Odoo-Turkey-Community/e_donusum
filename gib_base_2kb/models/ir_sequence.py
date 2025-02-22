# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import api, fields, models, Command
from odoo.exceptions import UserError


class IrSequence(models.Model):

    _inherit = "ir.sequence"

    gib_profile_type = fields.Selection(
        selection=[
            ("e-arsv", "E-Arşiv"),
            ("e-inv", "E-Fatura"),
        ],
        string="Fatura Türü",
    )
    gib_profile_id = fields.Many2many(
        comodel_name="gib_base_2kb.code",
        string="Fatura Senaryosu",
        help="Serinin kullanılacağı GİB Profillerini buradan ekleyebilirsiniz",
        domain="[('type', '=', 'profile_id'), ('value2', 'in', [gib_profile_type])]",
    )
    locked_sequence = fields.Boolean(copy=False)

    use_for_electronic = fields.Boolean("Elektronik")

    def _validate_electronic_sequence(self):
        """Elektronik fatura seri numarası için validasyon kontrolleri"""
        self.ensure_one()
        self.prefix = self.prefix or ""

        if "ABC" in self.prefix:
            raise UserError(
                "Lütfen Önek kısmında ki YALNIZCA ABC ön ekini geçerli bir seri ile değiştiriniz!"
            )

        if len(self.prefix) == 3:
            self.prefix += "%(range_year)s"
        else:
            if "%(range_year)s" not in self.prefix:
                self.prefix = ""
                if len(self.name) == 3:
                    self.prefix = self.name.upper() + "%(range_year)s"
                else:
                    self.prefix += "%(range_year)s"
            elif self.prefix == "%(range_year)s":
                if len(self.name) == 3:
                    self.prefix = self.name.upper() + "%(range_year)s"
            elif len(self.prefix) != 17:
                raise UserError(
                    "Elektronik fatura serilerinde 3 alfanümerik karakter olmalı!"
                )

        if self.use_for_electronic:
            self.locked_sequence = True

    @api.model_create_multi
    def create(self, vals_list):
        res_ids = super().create(vals_list)
        for res_id in res_ids.filtered(lambda x: x.use_for_electronic):
            res_id._validate_electronic_sequence()
        return res_ids

    def write(self, vals):
        res = super().write(vals)
        if 'prefix' in vals or 'use_for_electronic' in vals:
            for record in self.filtered(lambda x: x.use_for_electronic):
                record._validate_electronic_sequence()
        return res
