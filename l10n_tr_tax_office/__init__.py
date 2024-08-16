# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import os
import urllib
from lxml import etree

from . import models
from . import wizard


def post_init_hook(env):
    file_path = os.path.dirname(os.path.realpath(__file__))
    file = urllib.parse.urljoin('file:', os.path.join(file_path, 'data', 'Kodlar.xml'))
    root = etree.parse(file).getroot()
    xml_string = etree.tostring(root, pretty_print=True, encoding='unicode')

    env['account.tax.office.import'].turkey_tax_office_ebyn_import(xml_string)
