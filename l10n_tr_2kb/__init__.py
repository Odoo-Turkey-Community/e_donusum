# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import psycopg2
import logging

from . import models

from odoo import api, SUPERUSER_ID


_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    taxes_to_inactivate = [
        'l10n_tr.tr_kdv_satis_sale_18',
        'l10n_tr.tr_kdv_satis_purchase_18',
        'l10n_tr.tr_kdv_satis_sale_20',
        'l10n_tr.tr_kdv_satis_purchase_20'
    ]

    # Ön tanımlı gelen vergi şablonlarını arşivle
    for tax in taxes_to_inactivate:
        tax_obje = env.ref(tax, False)
        if tax_obje:
            tax_obje.action_archive()
