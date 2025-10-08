# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Kıta API kimlik bilgileri
    kita_api_key = fields.Char(
        string="Kıta API Key",
        related='company_id.kita_api_key',
        readonly=False,
        help="Kıta Yazılım'dan alınan API anahtarı"
    )

    kita_api_secret = fields.Char(
        string="Kıta API Secret",
        related='company_id.kita_api_secret',
        readonly=False,
        help="Kıta Yazılım'dan alınan API gizli anahtarı"
    )

    kita_api_base_url = fields.Char(
        string="Kıta API Base URL",
        related='company_id.kita_api_base_url',
        default="https://services.kitayazilim.com.tr",
        readonly=False,
        help="Kıta Yazılım API base URL"
    )
