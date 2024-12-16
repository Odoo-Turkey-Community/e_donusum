# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "Türkiye Vergi Daireleri 2KB",
    "version": "1.0",
    "summary": "Partner detayında kullanabileceğiniz Türkiyenin güncel vergi daireleri listesini ekler",
    "description": """
Türkiye Vergi Daireleri 2KB
===========================

Bu modül, Odoo'ya Türkiye'deki tüm vergi dairelerinin güncel listesini ekler ve 
iş ortakları (partner) için vergi dairesi yönetimini sağlar.

Özellikler:
-----------
* Türkiye'deki tüm vergi dairelerinin güncel listesi
* İş ortağı formunda vergi dairesi seçimi
* Şirket kartında vergi dairesi tanımlama
* Vergi dairesi listesi içe aktarma sihirbazı
* İl ve ilçe bazında vergi dairesi filtreleme

Teknik Özellikler:
-----------------
* Vergi daireleri için özel görünümler ve formlar
* Otomatik veri içe aktarma desteği
* Güvenlik erişim kuralları (ir.model.access)
* İş ortağı (res.partner) ve şirket (res.company) formlarına entegrasyon

Not: Bu modül, Türkiye'deki yasal gereksinimler için gerekli olan vergi dairesi 
bilgilerini yönetmenizi sağlar ve e-Fatura, e-İrsaliye gibi e-Belge süreçlerinde 
kullanılabilir.
    """,
    "maintainer": "Quanimo",
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://2kb.com.tr",
    "license": "Other proprietary",
    "sequence": 1453,
    "category": "Localization",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "views/account_tax_office_views.xml",
        "views/res_company_views.xml",
        "views/res_partner_views.xml",
        "wizard/account_tax_office_import_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
    "auto_install": False,
    "external_dependencies": {
        "python": [],
    },
    "images": ["images/main_screenshot.png"],
}
