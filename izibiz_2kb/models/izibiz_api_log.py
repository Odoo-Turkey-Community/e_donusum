# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import fields, models


class IzibizApiLog(models.Model):

    _name = "izibiz.api.log"
    _description = "Izibiz Api Log"

    name = fields.Char("kodu")
    desc = fields.Char("Açıklama")
    operation = fields.Char("Api")
    blocking_level = fields.Char("Hata Seviyesi")
    long_desc = fields.Text("Hata Mesajı")
    inovice_id = fields.Many2one(string="Fatura", comodel_name="account.move")
