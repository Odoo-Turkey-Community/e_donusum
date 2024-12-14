# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

{
    "name": "E-Dönüşüm Altyapısı",
    "summary": """Kıta yazılım tarafından geliştirilen bu uygulama ile odoo eskosisteminiz e-dönüşüme hazırlanır""",
    "description": """
        E-Dönüşüm süreçleri için temel altyapı modülüdür.
        Özellikler:
        * GİB (Gelir İdaresi Başkanlığı) entegrasyonu için temel yapılandırmalar
        * E-Belge süreçleri için ortak kullanılan fonksiyonlar
        * Entegratör bağlantıları için altyapı
        * Belge numaralama ve sıralama sistemleri
        * GİB servisleri ile iletişim için güvenlik protokolleri
        * Çoklu entegratör desteği
    """,
    "version": "1.0",
    "license": "Other proprietary",
    "maintainer": "Quanimo",
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://2kb.com.tr",
    "depends": ["account", "account_edi", "l10n_tr_2kb", "activation_2kb"],
    "data": [
        "security/ir.model.access.csv",
        "security/gib_provider.xml",
        "views/gib_local_menu.xml",
        "views/ir_sequence.xml",
        "views/res_partner.xml",
        "data/gib_base_2kb_code.xml",
        "data/gib_base_2kb_status_code.xml",
        "views/gib_provider.xml",
    ],
    "demo": [],
    "application": True,
    "images": ["images/main_screenshot.png"],
}
