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

    @api.model_create_multi
    def create(self, vals_list):
        res_ids = super().create(vals_list)
        for res_id in res_ids:
            res_id.prefix = res_id.prefix or ""
            if "ABC" in res_id.prefix:
                raise UserError(
                    "Lütfen Önek kısmında ki YALNIZCA ABC ön ekini geçerli bir seri ile değiştiriniz!"
                )

            if len(res_id.prefix) == 3:
                res_id.prefix += "%(range_year)s"
            else:
                if "%(range_year)s" not in res_id.prefix:
                    res_id.prefix = ""
                    if len(res_id.name) == 3:
                        res_id.prefix = res_id.name.upper() + "%(range_year)s"
                    else:
                        res_id.prefix += "%(range_year)s"
                elif res_id.prefix == "%(range_year)s":
                    if len(res_id.name) == 3:
                        res_id.prefix = res_id.name.upper() + "%(range_year)s"
                elif len(res_id.prefix) != 17:
                    raise UserError(
                        "Elektronik fatura serilerinde 3 alfanümerik karakter olmalı!"
                    )

            if res_id.use_for_electronic:
                res_id.locked_sequence = True
        return res_ids
