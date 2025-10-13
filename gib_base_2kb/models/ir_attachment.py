# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import fields, models


class IrAttachment(models.Model):

    _inherit = "ir.attachment"

    gib_profile_id = fields.Many2many(
        comodel_name="gib_base_2kb.code",
        string="GİB Profili",
        help="Şablonun kullanılacağı GİB Profillerini buradan ekleyebilirsiniz",
        domain="[('type', '=', 'profile_id')]",
    )
    gib_profile_id_value2 = fields.Char(
        related="gib_profile_id.value2", string="GİB Profili Değeri 2", readonly=True
    )

    use_for_electronic = fields.Boolean("Elektronik")
