# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    'name': 'Turkey Tax Offices',
    "version": "1.0",
    'summary': 'Turkey Tax Offices',
    'description': """
        Turkey Tax Offices
    """,

    "maintainer": "Quanimo",
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://2kb.com.tr",
    'license': 'Other proprietary',
    'sequence': 1453,

    "category": "Localization",

    'depends': [
        'account'
    ],

    'data': [
        'security/ir.model.access.csv',

        'views/account_tax_office_views.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',

        'wizard/account_tax_office_import_views.xml'
    ],

    'post_init_hook': 'post_init_hook',

    "installable": True,
    'application': False,
    'auto_install': False,

    'external_dependencies': {
        'python': [],
    },
    'images': ['images/main_screenshot.png']
}
