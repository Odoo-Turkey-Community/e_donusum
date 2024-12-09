# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import models


class GibUblTR12(models.AbstractModel):
    _inherit = "gib.ubl.tr12"

    def _export_invoice_vals(self, invoice):
        result = super()._export_invoice_vals(invoice)
        if invoice.gib_provider_id.provider == "izibiz":
            result["vals"].update(
                {
                    "signature_vals": {
                        "id_attrs": {"schemeID": "VKN_TCKN"},
                        "id": "4840847211",
                        "digital_signature_uri": "#Signature_" + invoice.gib_invoice_name,
                        "party_vals": {
                            "party_identification_vals": [
                                {"id": "4840847211", "id_attrs": {"schemeID": "VKN"}}
                            ],
                            "postal_address_vals": {
                                "street_name": "Altayçeşme Mh. Çamlı Sk. DAP Royal Center A Blok Kat15",
                                "city_subdivision_name": "MALTEPE",
                                "postal_zone": "34843",
                                "city_name": "ISTANBUL",
                                "country_name": "TR",
                            },
                        },
                    },
                }
            )
        return result
