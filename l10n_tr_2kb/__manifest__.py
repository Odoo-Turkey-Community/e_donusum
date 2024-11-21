# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

{
    "name": "Türkiye Lokalizasyonu Genişletmesi 2KB",
    "version": "1.0",
    "summary": "Türkiye Lokalizasyonu Genişletmesi 2KB",
    "description": """
        Türkiye Lokalizasyonu Genişletmesi 2KB
    """,
    "maintainer": "Quanimo",
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://2kb.com.tr",
    "license": "Other proprietary",
    "sequence": 1453,
    "category": "Accounting/Localizations/Account Charts",
    "depends": ["account"],
    "data": [
        "views/account_fiscal_position_views.xml",
        "views/account_tax_group_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": True,
    "external_dependencies": {
        "python": [],
    },
    "images": ["images/main_screenshot.png"],
}
