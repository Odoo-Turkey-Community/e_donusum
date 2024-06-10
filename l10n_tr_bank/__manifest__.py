# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

{
    "name": "Türkiye Bankaları",
    "version": "1.0",
    "summary": """
        Türkiye Bankaları""",
    "description": """
    Türkiye Cumhuriyetinde hali hazırda faal olan bütün bankalar adres ve iletişim bilgileri ile birlikte.
    """,
    "maintainer": "Quanimo",
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://2kb.com.tr",
    'license': 'Other proprietary',
    "sequence": 1453,
    "category": "account",
    "depends": [
        "account",
    ],
    "data": [
        "data/res_bank.xml", 
        "views/partner_views.xml", 
        "views/res_bank_views.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    'images': ['images/main_screenshot.png']
}
