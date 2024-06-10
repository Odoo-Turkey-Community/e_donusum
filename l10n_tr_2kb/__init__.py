# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import psycopg2
import logging

from . import models

from odoo import api, SUPERUSER_ID
from odoo.addons.account.models.chart_template import update_taxes_from_templates


_logger = logging.getLogger(__name__)

# def tax_and_account_template_ref(env, tax_templates, account_templates, company):
#     tax_template_ref = {}
#     for taxt in tax_templates:
#         modul, taxt_xml_id = taxt.get_external_id().get(taxt.id).split(".")
#         tax_template_ref.update({
#             taxt: env.ref(f'{modul}.{company.id}_{taxt_xml_id}')
#         })

#     account_template_ref = {}
#     for account in account_templates:
#         modul, account_xml_id = account.get_external_id().get(account.id).split(".")
#         account_template_ref.update({
#             account: env.ref(f'{modul}.{company.id}_{account_xml_id}')
#         })
#     return tax_template_ref, account_template_ref

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    taxes_to_inactivate = [
        'l10n_tr.tr_kdv_satis_sale_18',
        'l10n_tr.tr_kdv_satis_purchase_18',
        'l10n_tr.tr_kdv_satis_sale_20',
        'l10n_tr.tr_kdv_satis_purchase_20'
    ]

    # Ön tanımlı gelen vergi şablonlarını arşivle
    for tax in taxes_to_inactivate:
        tax_obje = env.ref(tax, False)
        if tax_obje:
            tax_obje.action_archive()

    # Kullanıcı kendi yüklese daha iyi olur sanki
    # l10n_tra = env.ref('l10n_tr.chart_template_7a', False)
    # l10n_tra.with_context(force=True).try_loading()

    # new_accounts = [
    #     '191010801', '191010808', '191010810', '191010818', '191010820',
    #     '191010901', '191010908', '191010910', '191010918', '191010920',
    #     '191011001', '191011008', '191011010', '191011018', '191011020',
    #     '191020101', '191020108', '191020110', '191020118', '191020120',
    #     '391000001', '391000008', '391000010', '391000018', '391000020',
    #     '391000101', '391000108', '391000110', '391000118', '391000120',
    #     '391000201', '391000208', '391000210', '391000218', '391000220',
    #     '360000001', '360000002', '360000003', '360000004', '360000005',
    #     '360000006', '360000007', '360000008', '360000009', '360000010'
    # ]

    # account_code_templates = {account_code: env.ref(f'l10n_tr_2kb.tr{account_code}') for account_code in new_accounts}

    # l10n_tr = env.ref('l10n_tr.chart_template_common', False)
    # l10n_tra = env.ref('l10n_tr.chart_template_7a', False)
    # l10n_trb = env.ref('l10n_tr.chart_template_7b', False)

    # companies = env['res.company'].search([('chart_template_id', 'in', [l10n_tr.id, l10n_tra.id, l10n_trb.id])])

    # tax_templates = env['account.tax.template'].with_context(active_test=False).search([('chart_template_id', '=', l10n_tr.id)])
    # account_templates = env['account.account.template'].with_context(active_test=False).search([('chart_template_id', '=', l10n_tr.id)])

    # for company in companies:
    #     # Ön tanımlı gelen vergileri arşivle
    #     taxes_to_inactivate = [
    #         f'{company.id}_tr_kdv_satis_sale_18',
    #         f'{company.id}_tr_kdv_satis_purchase_18',
    #         f'{company.id}_tr_kdv_satis_sale_20',
    #         f'{company.id}_tr_kdv_satis_purchase_20'
    #     ]
    #     for xml_id in taxes_to_inactivate:
    #         cr.execute("UPDATE account_tax SET active=False "
    #                    "WHERE id=(SELECT res_id FROM ir_model_data WHERE module = 'l10n_tr' AND name=%s)", (xml_id,))
    #     # Yeni hesapları ekle
    #     try:
    #         for account_code, account_template in account_code_templates.items():
    #             template_vals = [(account_template, company.chart_template_id._get_account_vals(company, account_template, account_code, {}))]
    #             company.chart_template_id._create_records_with_xmlid('account.account', template_vals, company)

    #             _logger.info("Created new accounts for company: %s(%s).", company.name, company.id)
    #     except psycopg2.errors.UniqueViolation:
    #         _logger.error("New accounts already exist for company: %s(%s).", company.name, company.id)

    # update_taxes_from_templates(cr, 'l10n_tr.chart_template_common')

    # # Yeni hesaplar ve vergiler oluştuktan sonra mali koşulları oluştur
    # for company in companies:
    #     # Template kayıt eşleşmesi
    #     tax_template_ref, account_template_ref = tax_and_account_template_ref(env, tax_templates, account_templates, company)
    #     # Mali koşulları oluştur
    #     l10n_tr.generate_fiscal_position(tax_template_ref, account_template_ref, company)
