# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

{
    'name': 'Turkey Localization Extension',
    "version": "1.0",
    'summary': 'Turkey Localization Extension',
    'description': """
        Turkey Localization Extension
    """,

    'maintainer': 'Quanimo',
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://2kb.com.tr",
    'license': 'Other proprietary',
    'sequence': 1453,

    'category': 'Accounting/Localizations/Account Charts',

    'depends': [
        'l10n_tr'
    ],

    'data': [
        'data/account_chart_template_data.xml',
        'data/account.account.template-common.csv',
        'data/account_tax_group_data.xml',
        'data/account_tax_template_base_data.xml',
        'data/accoun_fiscal_position_template_data_3xx.xml',
        'data/account_fiscal_position_tax_template.xml',

        'views/account_fiscal_position_views.xml',
        'views/account_tax_group_views.xml'
    ],

    "installable": True,
    'application': False,
    'auto_install': True,

    'post_init_hook': 'post_init_hook',

    'external_dependencies': {
        'python': [],
    },
    'images': ['images/main_screenshot.png']
}
