# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

{
    "name": "2KB Aktivasyon",
    "version": "1.0",
    "description": """
        2KB E-Dönüşüm ürün ailesi için lisans aktivasyon modülüdür.
        Özellikler:
        * Şirket bazlı lisans yönetimi
        * Otomatik lisans doğrulama
        * Güvenli şifreleme algoritmaları ile lisans kontrolü
        * Modül bazlı lisanslama desteği
    """,
    "summary": """ 2KB Aktivasyon uygulaması ile 2kb ürünlerinizin lisans akivasyon süreçlerini tamamlayabilirsiniz """,
    "maintainer": "Quanimo, Kıta",
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://2kb.com.tr",
    "license": "Other proprietary",
    "sequence": 1453,
    "category": "Hidden/Tools",
    "depends": ["base"],
    "data": ["views/res_company_views.xml"],
    "application": False,
    "installable": True,
    "auto_install": False,
    "external_dependencies": {
        "python": [
            "cryptography",
            "pycryptodome"
        ],
    },
    "images": ["images/main_screenshot.png"],
}
