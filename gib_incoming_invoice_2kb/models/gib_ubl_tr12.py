# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import re

from lxml import etree
from odoo import _, api, fields, models
from odoo.osv import expression


class GibUblTr12(models.AbstractModel):

    _inherit = "gib.ubl.tr12"

    # -------------------------------------------------------------------------
    # IMPORT INVOICE
    # -------------------------------------------------------------------------

    def _find_value(self, xpath, xml_element, namespaces=None):
        element = xml_element.xpath(xpath, namespaces=namespaces)
        return element[0].text if element else None

    # flake8: noqa: C901
    def _retrieve_partner(
        self, name=None, phone=None, mail=None, vat=None, domain=None
    ):
        """Search all partners and find one that matches one of the parameters.

        :param name:    The name of the partner.
        :param phone:   The phone or mobile of the partner.
        :param mail:    The mail of the partner.
        :param vat:     The vat number of the partner.
        :returns:       A partner or an empty recordset if not found.
        """

        def search_with_vat(extra_domain):
            if not vat:
                return None

            # Sometimes, the vat is specified with some whitespaces.
            normalized_vat = vat.replace(" ", "")
            country_prefix = re.match("^[A-Z]{2}|^", vat, re.I).group()

            partner = self.env["res.partner"].search(
                extra_domain + [("vat", "in", (normalized_vat, vat))], limit=1
            )

            # Try to remove the country code prefix from the vat.
            if not partner and country_prefix:
                partner = self.env["res.partner"].search(
                    extra_domain
                    + [
                        ("vat", "in", (normalized_vat[2:], vat[2:])),
                        ("country_id.code", "=", country_prefix.upper()),
                    ],
                    limit=1,
                )

                # The country could be not specified on the partner.
                if not partner:
                    partner = self.env["res.partner"].search(
                        extra_domain
                        + [
                            ("vat", "in", (normalized_vat[2:], vat[2:])),
                            ("country_id", "=", False),
                        ],
                        limit=1,
                    )

            # The vat could be a string of alphanumeric values without country code but with missing zeros at the
            # beginning.
            if not partner:
                try:
                    vat_only_numeric = str(
                        int(re.sub(r"^\D{2}", "", normalized_vat) or 0)
                    )
                except ValueError:
                    vat_only_numeric = None

                if vat_only_numeric:
                    query = self.env["res.partner"]._where_calc(
                        extra_domain + [("active", "=", True)]
                    )
                    tables, where_clause, where_params = query.get_sql()

                    if country_prefix:
                        vat_prefix_regex = f"({country_prefix})?"
                    else:
                        vat_prefix_regex = "([A-Z]{2})?"

                    self._cr.execute(
                        f"""
                        SELECT res_partner.id
                        FROM {tables}
                        WHERE {where_clause}
                        AND res_partner.vat ~* %s
                        LIMIT 1
                    """,
                        where_params
                        + ["^%s0*%s$" % (vat_prefix_regex, vat_only_numeric)],
                    )
                    partner_row = self._cr.fetchone()
                    if partner_row:
                        partner = self.env["res.partner"].browse(partner_row[0])

            return partner

        def search_with_phone_mail(extra_domain):
            domains = []
            if phone:
                domains.append([("phone", "=", phone)])
                domains.append([("mobile", "=", phone)])
            if mail:
                domains.append([("email", "=", mail)])

            if not domains:
                return None

            domain = expression.OR(domains)
            if extra_domain:
                domain = expression.AND([domain, extra_domain])
            return self.env["res.partner"].search(domain, limit=1)

        def search_with_name(extra_domain):
            if not name:
                return None
            return self.env["res.partner"].search(
                [("name", "ilike", name)] + extra_domain, limit=1
            )

        def search_with_domain(extra_domain):
            if not domain:
                return None
            return self.env["res.partner"].search(domain + extra_domain, limit=1)

        for search_method in (
            search_with_vat,
            search_with_domain,
            search_with_phone_mail,
            search_with_name,
        ):
            for extra_domain in ([("company_id", "=", self.env.company.id)], []):
                partner = search_method(extra_domain)
                if partner:
                    return partner

        return self.env["res.partner"]
