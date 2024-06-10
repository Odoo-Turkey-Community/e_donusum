# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import time
from odoo import fields, Command
from odoo.tests.common import TransactionCase, HttpCase, tagged, Form


class EntegratorCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create user.
        user = cls.env["res.users"].create(
            {
                "name": "Because I am accountman!",
                "login": "accountman",
                "password": "accountman",
                "groups_id": [
                    (6, 0, cls.env.user.groups_id.ids),
                    (4, cls.env.ref("account.group_account_manager").id),
                    (4, cls.env.ref("account.group_account_user").id),
                ],
            }
        )
        user.partner_id.email = "accountman@test.com"

        # Shadow the current environment/cursor with one having the report user.
        # This is mandatory to test access rights.
        cls.env = cls.env(user=user)
        cls.cr = cls.env.cr

        # ==== Products ====
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product Product 4",
                "standard_price": 500.0,
                "list_price": 750.0,
                "type": "consu",
                "categ_id": cls.env.ref("product.product_category_all").id,
            }
        )

        # ==== alias ====
        cls.alias_inv_gb = cls.env["gib_base_2kb.alias"].create(
            {
                "vkn_tckn": "1234567802",
                "title": "DİASERTİFİKA1 DEĞİŞTİRMEYELİM",
                "alias": "urn:mail:merkezgb@nes.com.tr",
                "document_type": "invoice",
                "role": "GB",
            }
        )

        cls.alias_inv_pk_1 = cls.env["gib_base_2kb.alias"].create(
            {
                "vkn_tckn": "1234567801",
                "title": "DİATESTTEST DEĞİşTiRMEYELİM",
                "alias": "urn:mail:defaultpk@nes.com.tr",
                "document_type": "invoice",
                "role": "PK",
            }
        )

        cls.alias_irs_pk_1 = cls.env["gib_base_2kb.alias"].create(
            {
                "vkn_tckn": "1234567801",
                "title": "DİATESTTEST DEĞİşTiRMEYELİM",
                "alias": "urn:mail:merkezpk@nes.com.tr",
                "document_type": "despatchadvice",
                "role": "PK",
            }
        )

        # ==== Partners ====
        cls.partner_e_inv = cls.env["res.partner"].create(
            {
                "name": "partner_a",
                "vat": "1234567801",
                "alias_pk": cls.alias_inv_pk_1.id,
                "company_id": False,
            }
        )

        cls.partner_e_irs = cls.env["res.partner"].create(
            {
                "name": "partner_a",
                "vat": "1234567801",
                "alias_despatch_pk": cls.alias_irs_pk_1.id,
                "company_id": False,
            }
        )

        cls.partner_e_arsv = cls.env["res.partner"].create(
            {
                "name": "partner_b",
                "property_payment_term_id": cls.pay_terms_b.id,
                "property_supplier_payment_term_id": cls.pay_terms_b.id,
                "property_account_position_id": cls.fiscal_pos_a.id,
                "property_account_receivable_id": cls.company_data[
                    "default_account_receivable"
                ]
                .copy()
                .id,
                "property_account_payable_id": cls.company_data[
                    "default_account_payable"
                ]
                .copy()
                .id,
                "company_id": False,
            }
        )

        cls.company_tr = cls.env["res.company"].create(
            {
                "country_id": cls.env.ref("base.au").id,
                "currency_id": cls.env.ref("base.AUD").id,
                "email": "company.2@test.example.com",
                "name": "New Test Company",
            }
        )

        cls.journal_e_inv = cls.env["account.journal"].create(
            {
                "name": "e-Fatura",
                "type": "sale",
                "code": "JXX",
                "currency_id": cls.currency_usd_id,
                "gib_provider_id": cls.env.ref("nes.provider-nes_sunucu_1").id,
                "gib_invoice_type": "e-inv",  # e-arsv, e-inv
            }
        )

        cls.journal_e_arsv = cls.env["account.journal"].create(
            {
                "name": "e-Arşiv",
                "type": "sale",
                "code": "JYY",
                "currency_id": cls.currency_usd_id,
                "gib_provider_id": cls.env.ref("nes.provider-nes_sunucu_1").id,
                "gib_invoice_type": "e-arsv",
            }
        )

    def _create_invoice(
        self,
        move_type="out_invoice",
        invoice_amount=50,
        currency_id=None,
        partner_id=None,
        date_invoice=None,
        payment_term_id=False,
        auto_validate=False,
    ):
        date_invoice = date_invoice or time.strftime("%Y") + "-07-01"

        invoice_vals = {
            "move_type": move_type,
            "partner_id": partner_id or self.partner_agrolait_id,
            "invoice_date": date_invoice,
            "date": date_invoice,
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "name": "product that cost %s" % invoice_amount,
                        "quantity": 1,
                        "price_unit": invoice_amount,
                        "tax_ids": [Command.set([])],
                    },
                )
            ],
        }

        if payment_term_id:
            invoice_vals["invoice_payment_term_id"] = payment_term_id

        if currency_id:
            invoice_vals["currency_id"] = currency_id

        invoice = (
            self.env["account.move"]
            .with_context(default_move_type=move_type)
            .create(invoice_vals)
        )
        if auto_validate:
            invoice.action_post()
        return invoice

    def create_invoice(
        self, move_type="out_invoice", invoice_amount=50, currency_id=None
    ):
        return self._create_invoice(
            move_type=move_type,
            invoice_amount=invoice_amount,
            currency_id=currency_id,
            auto_validate=True,
        )

    def create_invoice_partner(
        self,
        move_type="out_invoice",
        invoice_amount=50,
        currency_id=None,
        partner_id=False,
        payment_term_id=False,
    ):
        return self._create_invoice(
            move_type=move_type,
            invoice_amount=invoice_amount,
            currency_id=currency_id,
            partner_id=partner_id,
            payment_term_id=payment_term_id,
            auto_validate=True,
        )
