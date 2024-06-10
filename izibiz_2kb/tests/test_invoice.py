# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from unittest.mock import patch

from odoo.addons.nes.tests.common import EntegratorCommon

from odoo.tests import tagged
from odoo.exceptions import UserError, ValidationError


class TestEntegrator(EntegratorCommon):

    def test_create_invoice(self):
        pass
