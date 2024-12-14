# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

{
    "name": "Türkiye - Vergi, Vergi Grupları ve Mali Koşulları 2KB",
    "version": "1.0",
    "category": "Accounting/Localizations/Account Charts",
    'description': """
Türkiye - Vergi ve Mali Koşulları
=================================

Bu modül, Türkiye'deki işletmeler için gerekli mali koşulları ve mali koşulları ekler:

Özellikler:
-----------
* Türkiye'ye özgü mali koşullar
* Stopaj ve tevkifat uygulamaları için özel vergi grupları
* KDV tevkifatı için özel vergi hesaplamaları
* 2/10, 3/10, 4/10, 5/10, 7/10, 9/10 gibi KDV tevkifat oranları
* Gelir ve kurumlar vergisi stopaj oranları

Teknik Detaylar:
---------------
* Vergi grupları için özel görünümler
* Mali koşullar için özelleştirilmiş formlar
* Otomatik vergi hesaplamaları ve maplemeler

Not: Bu modül Türkiye'deki yasal vergi gereksinimlerine uygun olarak tasarlanmıştır ve 
resmi Türk muhasebe planı (l10n_tr) ile entegre çalışır.
    """,
    "maintainer": "Quanimo",
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://2kb.com.tr",
    "sequence": 1453,
    'depends': [
        "l10n_tr",
    ],
    'data': [
        'views/account_fiscal_position_views.xml',
        'views/account_tax_group_views.xml'
    ],
    'license': "LGPL-3",
    "installable": True,
    "application": False,
    "auto_install": True,
    "images": ["images/main_screenshot.png"],
}
