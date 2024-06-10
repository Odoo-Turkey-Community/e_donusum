# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import fields, models


class GibCode(models.Model):

    _name = "gib_base_2kb.code"
    _description = "Gib Kod List"

    name = fields.Char("Kod", required=True)
    short_name = fields.Char("Kısa Kod")
    type = fields.Char("Kategori", required=True)
    value = fields.Char("Değer")
    value2 = fields.Char("EK Değer1")
    value3 = fields.Char("EK Değer2")
    active = fields.Boolean("Aktif", default=True)

    _sql_constraints = [
        ("type_code_uniq", "unique (type,name)", "Kod kategoride tekil olmalı!")
    ]
