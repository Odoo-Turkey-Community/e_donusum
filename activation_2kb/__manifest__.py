# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

{
    'name': '2KB Activation',
    "version": "1.0",
    'description': """ 2KB Activation """,
    'summary': """ 2KB Activation """,

    'maintainer': 'Quanimo, Kıta',
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://github.com/Odoo-Turkey-Community",
    'license': 'Other proprietary',
    'sequence': 1453,

    'category': 'Hidden/Tools',
    'depends': ['base'],
    "data": [
        "views/res_company_views.xml"
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
        'python': [
            'cryptography',
            'pycryptodome==3.20.0'
        ],
    }
}
