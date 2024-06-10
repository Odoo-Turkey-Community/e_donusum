# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

{
    "name": "İZİBİZ E-Dönüşüm Sağlayıcısı",
    "version": "16.0.0.0.1",
    "summary": "İZİBİZ E-Dönüşüm Sağlayıcısı",
    "description": """
        İZİBİZ E-Dönüşüm Sağlayıcısı
    """,
    "version": "1.0",
    'maintainer': 'Quanimo',
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://github.com/Odoo-Turkey-Community",
    'license': 'Other proprietary',
    "sequence": 1453,
    "category": "Accounting/Localizations/Account Charts",
    "depends": ["gib_base_2kb", "gib_invoice_2kb"],
    "data": [
        "security/izibiz_api_log.xml",
        "data/gib_provider.xml",
        "views/gib_provider.xml",
    ],
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
