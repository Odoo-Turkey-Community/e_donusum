# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

{
    "name": "Türkiye Bankaları 2KB",
    "version": "1.0",
    "summary": """
        Türkiye Bankaları""",
    "description": """
Türkiye Lokalizasyonu Temel 2KB
===============================

Bu modül, Türkiye'deki işletmeler için temel lokalizasyon özelliklerini içerir:

* Resmi Türk muhasebe planı entegrasyonu (l10n_tr)
* Stopaj ve vergi tevkifatı işlemleri (l10n_tr_witholding)
* Türk bankaları entegrasyonu (l10n_tr_bank)
* Türkiye vergi dairesi entegrasyonu (l10n_tr_tax_office)

Özellikler:
-----------
* Türkiye'ye özgü vergi pozisyonları ve vergi grupları
* Stopaj işlemleri için özel vergi hesaplamaları
* Türk bankacılık sistemi entegrasyonu
* Vergi dairesi işlemleri ve raporlamaları

Not: Bu modül, Türkiye'deki yasal gereksinimler için gerekli olan temel lokalizasyon özelliklerini sağlar.
    """,
    "maintainer": "Quanimo",
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://2kb.com.tr",
    "license": "Other proprietary",
    "sequence": 1453,
    "category": "account",
    "depends": [
        "account",
    ],
    "data": [
        "data/res_bank.xml",
        "views/partner_views.xml",
        "views/res_bank_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["static/description/images/main_screenshot.png"],
}
