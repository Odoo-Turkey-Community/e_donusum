# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import api, fields, models


class GibUserAlias(models.Model):
    _name = "gib_base_2kb.alias"
    _description = "GibUser"
    _log_access = False
    _rec_name = "alias"

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        if name and name[:2].isalpha():
            name = name[2:]

        domain = domain or []
        for item in domain:
            if isinstance(item, list) and item[0] == 'vkn_tckn' and item[2][:2].isalpha():
                item[2] = item[2][2:]
        return super()._name_search(name, domain, operator, limit, order)

    vkn_tckn = fields.Char("VKN/TCKN", size=11, index=True)
    title = fields.Char("Ünvan")
    alias = fields.Char("Etiket")
    type = fields.Selection(
        selection=[
            ("OZEL", "Özel"),
            ("KAMU", "Kamu"),
        ]
    )
    creationTime = fields.Datetime(
        "Oluşturulma Tarihi"
    )  # TODO etikette kontrol amaçlı kullanılacak
    document_type = fields.Selection(
        selection=[("invoice", "e-Fatura"), ("despatchadvice", "e-İrsaliye")],
        string="Döküman Tipi",
    )
    role = fields.Selection(
        selection=[("PK", "Posta Kutusu"), ("GB", "Gönderici Birim")], string="Rol"
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "uniq_alias",
            "unique(vkn_tckn,document_type,role,alias)",
            """Etiket tekil olmalı""",
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        """Gelen data çakışmayı engellemek için ayıklanıyor"""
        domain = [
            ("vkn_tckn", "in", list(set([val.get("vkn_tckn") for val in vals_list])))
        ]
        exists_alias = self.search(domain)
        updated_vals_list = []
        for values in vals_list:
            if not exists_alias.filtered(
                lambda l: l.vkn_tckn == values.get("vkn_tckn")
                and l.document_type == values.get("document_type")
                and l.role == values.get("role")
                and l.alias == values.get("alias")
            ):
                updated_vals_list.append(values)
        return super().create(updated_vals_list)

    @api.model
    def get_pk_by_vat(self, vat, document_type="invoice"):
        """Gelen data çakışmayı engellemek için ayıklanıyor"""
        domain = [("vkn_tckn", "=", vat)]
        domain += [("document_type", "=", document_type)]
        domain += [("role", "=", "PK")]
        return self.search(domain)

    @api.model
    def get_gb_by_vat(self, vat, document_type="invoice"):
        """Gelen data çakışmayı engellemek için ayıklanıyor"""
        domain = [("vkn_tckn", "=", vat)]
        domain += [("document_type", "=", document_type)]
        domain += [("role", "=", "GB")]
        return self.search(domain)
