# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import re
from odoo import _, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):

    _inherit = "res.partner"

    # TODO : document_type kaldırılacak # her hangi bir modelde bağlantı bulunamadı kaldırılabilir
    document_type = fields.Selection(
        selection=[("invoice", "e-Fatura"), ("despatchadvice", "e-İrsaliye")],
        string="Döküman Tipi",
    )

    role = fields.Selection(
        selection=[("PK", "Posta Kutusu"), ("GB", "Gönderici Birim")], string="Rol"
    )

    last_gib_check = fields.Datetime(string="GIB Güncelleme")

    def clear_vat(self):
        if not self.vat:
            return self.vat
        return re.findall(r"\d+", self.vat)[0]

    def get_partner_alias(self):
        """Özel Entegratör üzerinden partner GIB etiket bilgilerini günceller"""
        if not self.vat:
            display_field_names = self.fields_get("vat")
            display_field = f"'{display_field_names['vat']['string']}'"
            raise UserError(
                _(
                    "The field %s is required on %s.",
                    display_field,
                    self.commercial_partner_id.display_name,
                )
            )

        gib_provider = self.env["gib_base_2kb.provider"].get_default_provider()
        if not gib_provider:
            raise UserError(_("Varsayılan entegratör gereklidir."))

        role = "GB" if self == self.env.company.partner_id else "PK"
        if role == "GB":
            result, alias = gib_provider._get_partner_alias(self.clear_vat(), role="GB")
        else:
            result, alias = gib_provider._get_partner_alias(self.clear_vat())

        if result:
            self.last_gib_check = fields.datetime.today()
            alias_to_create = []
            alias_to_update = {}
            alias_model = self.env["gib_base_2kb.alias"].sudo()
            partner_alias = alias_model.with_context(active_test=False).search(
                [("vkn_tckn", "=", self.clear_vat()), ("role", "=", role)]
            )
            for item in alias:
                elias_exists = partner_alias.filtered(
                    lambda alias: alias.document_type == item.get("document_type")
                    and alias.alias == item.get("alias")
                )
                if not elias_exists:
                    alias_to_create.append(item)
                elif not elias_exists.active:
                    alias_to_update[elias_exists.id] = {"active": True}
            for alias_id in partner_alias.filtered(lambda alias: alias.active):
                found = [
                    item
                    for item in alias
                    if item.get("alias") == alias_id.alias
                    and item.get("document_type") == alias_id.document_type
                ]
                if not found:
                    alias_to_update[alias_id.id] = {"active": False}

            for alias_id, values in alias_to_update.items():
                alias_model.browse(alias_id).write(values)

            if alias_to_create:
                alias_model.create(alias_to_create)
        return result, alias
