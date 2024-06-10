# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from lxml import etree
import base64
import logging

from odoo import fields, models

logger = logging.getLogger(__name__)


class AccountTaxOfficeImport(models.TransientModel):
    _name = 'account.tax.office.import'
    _description = "Account Tax Office Import"

    xml_file = fields.Binary('Tax Office XML', required=True)

    def import_xml(self):
        xml_file_string = base64.decodebytes(self.xml_file)
        self.turkey_tax_office_ebyn_import(xml_file_string)

    def turkey_tax_office_ebyn_import(self, xml_file_string):
        try:
            AccountTaxOffice = self.env['account.tax.office']

            parser = etree.XMLParser(recover=True)
            xml_root = etree.fromstring(xml_file_string, parser)
            namespaces = xml_root.nsmap

            tax_offices = xml_root.xpath("//vergidairesi", namespaces=namespaces)
            for tax_office in tax_offices:
                tax_name = tax_office.xpath("vdad", namespaces=namespaces)[0].text
                tax_code = tax_office.xpath("vdkod", namespaces=namespaces)[0].text
                country_code = tax_code[1:3] if tax_code else False

                country_state = self.env['res.country.state'].search([
                    ('country_id.code', '=', 'TR'),
                    ('code', '=', country_code)
                ], limit=1)

                tax_office_model = AccountTaxOffice.sudo().search([
                    ('code', '=', tax_code),
                ], limit=1)

                if tax_office_model.exists():
                    tax_office_model.sudo().write({
                        'name': tax_name,
                        'state_id': country_state.id if country_state else False
                    })
                else:
                    AccountTaxOffice.sudo().create({
                        'name': tax_name,
                        'code': tax_code,
                        'state_id': country_state.id if country_state else False
                    })

        except Exception as ex:
            logger.error('Account Tax Office Import XML Error: ' + str(ex))
