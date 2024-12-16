# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

{
    "name": "Gelen E-Faturaların Alınması",
    "summary": """2KB Türkiye lokalizasyon ekibi tarafından geliştirilmiştir. Gelen E-Faturaların Alınması ve incelenmesine olanak verir""",
    "description": """
        Gelen E-Fatura yönetimi için geliştirilmiş kapsamlı bir modüldür.
        Özellikler:
        * GİB üzerinden gelen E-Faturaların otomatik alımı
        * Gelen E-Faturaların Odoo faturalarına dönüştürülmesi
        * XML formatındaki faturaların görsel önizlemesi
        * Toplu fatura indirme ve işleme
        * Fatura red/kabul süreçlerinin yönetimi
        * Gelen fatura raporlaması ve analizi
    """,
    "version": "1.0",
    "maintainer": "Quanimo",
    "author": "Kıta, Quanimo, Broadmax",
    "website": "https://2kb.com.tr",
    "license": "Other proprietary",
    "depends": ["gib_invoice_2kb"],
    "data": [
        "security/gib_incoming_invoice.xml",
        "views/gib_incoming_invoice.xml",
    ],
    "demo": [],
    "images": ["images/main_screenshot.png"],
}
