# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

{
    "name": "E-Fatura ve E-Arşiv Konnektörü",
    "summary": """E-Fatura ve E-Arşiv için uygun ortamı uygulamanız için hazırlar""",
    "description": """
        E-Fatura ve E-Arşiv fatura oluşturma ve gönderme süreçlerini yöneten ana modüldür.
        Özellikler:
        * UBL-TR standardına uygun E-Fatura oluşturma
        * E-Arşiv fatura oluşturma ve raporlama
        * Toplu fatura gönderimi
        * Otomatik fatura numaralama
        * Fatura durumu takibi ve raporlama
        * E-Fatura ve E-Arşiv fatura şablonları
        * GİB'e uyumlu fatura senaryoları (Temel/Ticari)
        * Çoklu para birimi desteği
    """,
    "version": "1.0",
    "maintainer": "Quanimo",
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://2kb.com.tr",
    "license": "Other proprietary",
    "depends": [
        "gib_base_2kb",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/gib_base_2kb_code.xml",
        "views/account_journal_dashboard_view.xml",
        "views/account_move_views.xml",
        "views/gib_base_2kb_provider_views.xml",
        "views/res_partner.xml",
        "wizards/gib_invoice_restricted_cancel_wizard.xml",
        "wizards/gib_invoice_archive_cancel_wizard.xml",
    ],
    "demo": [],
    "images": ["images/main_screenshot.png"],
}
