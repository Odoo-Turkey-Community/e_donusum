# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

{
    "name": "Türkiye Bankaları 2KB",
    "version": "1.0",
    "summary": """
        Türkiye Bankaları""",
    "description": """
Türkiye Bankaları 2KB
====================

Bu modül, Türkiye'de faaliyet gösteren tüm bankaların güncel bilgilerini Odoo sisteminize ekler.

Özellikler:
-----------
* Türkiye'deki tüm aktif bankaların listesi
* Her banka için:
  - Banka şube bilgileri
  - SWIFT/BIC kodları
  - İletişim bilgileri (telefon, faks, e-posta)
  - Tam adres bilgileri
  - EFT ve IBAN kodları

Teknik Özellikler:
-----------------
* Banka kayıtları için özelleştirilmiş görünümler
* İş ortağı formlarında banka seçimi
* Hazır yüklenmiş banka verileri (res_bank.xml)
* Banka bilgileri için gelişmiş arama ve filtreleme

Entegrasyon:
-----------
* Muhasebe modülü ile tam entegrasyon
* Banka hesapları yönetimi
* Ödeme işlemleri için hazır banka bilgileri

Not: Bu modül, Türkiye'deki bankacılık işlemleriniz için gerekli olan tüm banka 
bilgilerini içerir ve düzenli olarak güncellenir.
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
    "images": ["images/main_screenshot.png"],
}
