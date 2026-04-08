# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

{
    "name": "E-Dönüşüm Altyapısı",
    "summary": """Hızla dijitalleşen Türkiye muhasebesine entegre olmanızı sağlayacak E-Dönüşüm Altyapısı uygulaması ile odoo nuz da dijitalleşmeye hazır hale gelir""",
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
    "version": "1.3",
    "license": "Other proprietary",
    "maintainer": "Quanimo",
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://2kb.com.tr",
    "depends": ["account", "account_edi", "l10n_tr_2kb", "kita_api_services"],
    "data": [
        "security/ir.model.access.csv",
        "security/gib_provider.xml",
        "data/gib_base_2kb_code.xml",
        "data/gib_base_2kb_status_code.xml",
        "data/uom_data.xml",
        "views/gib_local_menu.xml",
        "views/gib_provider.xml",
        "views/uom_uom_views.xml",
        "views/ir_sequence.xml",
        "views/res_company_views.xml",
        "views/res_partner.xml",
    ],
    "demo": [],
    "application": True,
    "images": ["static/description/images/main_screenshot.png"],
}
