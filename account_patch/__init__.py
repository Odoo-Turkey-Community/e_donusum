# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo.addons.account.models.chart_template import AccountChartTemplate


origin_try_loading = AccountChartTemplate.try_loading
AccountChartTemplate.origin_try_loading = origin_try_loading


def new_try_loading(self, company=False, install_demo=True):
    l10n_tr_chart = [
        self.env.ref("l10n_tr.chart_template_common", False),
        self.env.ref("l10n_tr.chart_template_7a", False),
        self.env.ref("l10n_tr.chart_template_7b", False),
    ]
    # İlk kurulumda force gelmemiş ise Türkiyenin muhasebe hesap ve vergilerini yükleme kullanıcı kendi seçsin
    if not self.env.context.get("force", False) and self in l10n_tr_chart:
        return
    return self.origin_try_loading(company, install_demo)


AccountChartTemplate.try_loading = new_try_loading
