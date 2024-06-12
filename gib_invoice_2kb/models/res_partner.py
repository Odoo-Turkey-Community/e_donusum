# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    alias_pk = fields.Many2one(
        "gib_base_2kb.alias",
        string="Alıcı Etiket",
        domain="[('role', '=', 'PK'),('document_type','=','invoice'),('vkn_tckn', '=', vat)]",
        copy=False,
    )
    profile_id = fields.Many2one(
        "gib_base_2kb.code",
        domain="[('type', '=', 'profile_id')]",
        string="Fatura Senaryosu",
    )
    sequence_id = fields.Many2one(
        "ir.sequence",
        string="Fatura Seri",
        help="Bu alan e-Dökümanlara verilecek ön tanımlı sıra numarasını olarak kullanılır",
        domain="[('gib_profile_id', 'in', [profile_id])]",
    )
    is_e_inv = fields.Boolean(string="e-Fatura Mükellefi", default=False, copy=False)

    def get_partner_alias(self):
        result, alias = super().get_partner_alias()

        if not result:
            return result, alias

        if self.alias_pk.vkn_tckn != self.clear_vat() or not self.alias_pk.active:
            self.alias_pk = False

        pk_id = self.env["gib_base_2kb.alias"].search(
            [
                ("vkn_tckn", "=", self.clear_vat()),
                ("document_type", "=", "invoice"),
                ("role", "=", "PK"),
            ],
            order="creationTime desc",
            limit=1,
        )

        if pk_id:
            self.is_e_inv = True
            if not self.profile_id or self.profile_id.value2 == "e-arsv":
                self.profile_id = self.env.ref(
                    "gib_invoice_2kb.profile_id-TICARIFATURA"
                ).id

            if not self.alias_pk:
                self.alias_pk = pk_id
        else:
            self.is_e_inv = False
            self.alias_pk = False
            self.profile_id = self.env.ref("gib_invoice_2kb.profile_id-EARSIVFATURA").id
        return result, alias

    @api.onchange("is_e_inv")
    def onchange_is_e_inv(self):
        if self.is_e_inv:
            return {"domain": {"profile_id": [("value2", "=", "e-inv")]}}
        else:
            self.profile_id = False
            return {"domain": {"profile_id": [("value2", "=", "e-arsv")]}}

    @api.onchange("vat")
    def onchange_vat(self):
        if not self.vat:
            self.is_e_inv = False
            self.alias_pk = False
            self.profile_id = False
        else:
            try:
                self.get_partner_alias()
            except Exception:
                pass
