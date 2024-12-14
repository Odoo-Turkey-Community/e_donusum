# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import logging

import requests
import json
import copy

from odoo import models, fields, api, _
from odoo.models import AbstractModel
from odoo.tools import float_repr
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_round
from odoo.addons.activation_2kb.tools.crypt_message import CryptEncrypteMessage

from datetime import datetime

DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_TIME_FORMAT = "%H:%M:%S"

# -------------------------------------------------------------------------
# UNIT OF MEASURE
# -------------------------------------------------------------------------
UOM_TO_UNECE_CODE = {
    "uom.product_uom_unit": "C62",
    # "uom.product_uom_unit": ["C62", "NIU"],
    "uom.product_uom_dozen": "DZN",
    "uom.product_uom_kgm": "KGM",
    "uom.product_uom_gram": "GRM",
    "uom.product_uom_day": "DAY",
    "uom.product_uom_hour": "HUR",
    "uom.product_uom_ton": "TNE",
    "uom.product_uom_meter": "MTR",
    "uom.product_uom_km": "KTM",
    "uom.product_uom_cm": "CMT",
    "uom.product_uom_litre": "LTR",
    "uom.product_uom_cubic_meter": "MTQ",
    "uom.product_uom_lb": "LBR",
    "uom.product_uom_oz": "ONZ",
    "uom.product_uom_inch": "INH",
    "uom.product_uom_foot": "FOT",
    "uom.product_uom_mile": "SMI",
    "uom.product_uom_floz": "OZA",
    "uom.product_uom_qt": "QT",
    "uom.product_uom_gal": "GLL",
    "uom.product_uom_cubic_inch": "INQ",
    "uom.product_uom_cubic_foot": "FTQ",
    "uom.product_uom_millimeter": "MTK",
    "uom.product_uom_yard": "YD",
}

_logger = logging.getLogger(__name__)


class GibUblTR12(models.AbstractModel):
    _name = "gib.ubl.tr12"
    _description = "UBL TR1.2"

    # -------------------------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------------------------
    def format_date(self, dt=False):
        dt = dt or datetime.now()
        return dt.strftime(DEFAULT_DATE_FORMAT)

    def format_time(self, dt=False):
        dt = dt or fields.Datetime.now()
        dt = fields.Datetime.context_timestamp(self, dt)
        return dt.strftime(DEFAULT_TIME_FORMAT)

    def format_float(self, amount, precision_digits):
        if amount is None:
            return False
        return float_repr(float_round(amount, precision_digits), precision_digits)

    def get_vat_number(self, vat):
        if not vat:
            return ""
        if vat[:2].isdecimal():
            return vat.replace(" ", "")
        return vat[2:].replace(" ", "")

    def get_vat_number_type(self, vat):
        return "TCKN" if vat and len(self.get_vat_number(vat)) == 11 else "VKN"

    def _get_uom_unece_code(self, product_uom):
        xmlid = product_uom.get_external_id()
        if xmlid and product_uom.id in xmlid:
            return UOM_TO_UNECE_CODE.get(xmlid[product_uom.id], "C62")
        return "C62"

    def _get_unece_code_from_uom(self, product_uom):
        try:
            return list(UOM_TO_UNECE_CODE.keys())[
                list(UOM_TO_UNECE_CODE.values()).index(product_uom)
            ]
        except Exception:
            return list(UOM_TO_UNECE_CODE.keys())[0]

    # -------------------------------------------------------------------------
    # EXPORT COMMON
    # -------------------------------------------------------------------------

    def _get_partner_party_identification_vals_list(self, partner):
        # TODO diğerleride eklencek
        vat = partner.vat or "1111111111"
        return [
            {
                "id": self.get_vat_number(vat),
                "id_attrs": {"schemeID": self.get_vat_number_type(vat)},
            }
        ]

    def _get_partner_address_vals(self, partner):
        postal_zone = partner.zip or (partner.state_id.code + "000")
        return {
            "street_name": " ".join(filter(None, (partner.street, partner.street2))),
            "city_subdivision_name": partner.city,
            "postal_zone": postal_zone,
            "city_name": partner.state_id.name,
            "country_name": partner.country_id.name or "Türkiye",
        }

    def _get_partner_party_tax_scheme_vals_list(self, partner, role):
        if "tax_office_id" in partner._fields:
            return [
                {
                    "tax_scheme_name": partner.tax_office_id.name,
                }
            ]
        return False

    def _get_partner_contact_vals(self, partner):
        return {
            "name": partner.name,
            "telephone": partner.phone or partner.mobile,
            "electronic_mail": partner.email,
        }

    def _get_partner_person_vals(self, partner):
        if self.get_vat_number_type(partner.vat) == "TCKN":
            return {
                "first_name": " ".join(partner.name.split()[:-1]),
                "family_name": " ".join(partner.name.split()[-1:]),
            }
        else:
            return {}

    def _get_partner_party_vals(self, partner, role):
        return {
            "website_uri": partner.website,
            "party_identification_vals": (
                [{"id": "EXPORT", "id_attrs": {"schemeID": "PARTYTYPE"}}]
                if role == "export"
                else self._get_partner_party_identification_vals_list(partner)
            ),
            "party_name_vals": [{"name": partner.commercial_partner_id.name}],
            "postal_address_vals": self._get_partner_address_vals(partner),
            "party_tax_scheme_vals": self._get_partner_party_tax_scheme_vals_list(
                partner, role
            ),
            "party_legal_entity_vals": [
                (
                    {
                        "registration_name": partner.commercial_partner_id.name,
                        "company_id": self.get_vat_number(
                            partner.commercial_partner_id.vat
                        ),
                    }
                    if role == "export"
                    else {}
                )
            ],
            "contact_vals": self._get_partner_contact_vals(partner),
            "person_vals": self._get_partner_person_vals(partner),
        }

    def get_authenticate_on_server(self, provider, app, vals):
        data = {
            "provider": provider.name,
            "vals": vals,
        }
        company = provider.company_id

        if not company.priv_key_2kb or not company.pub_key_2kb:
            raise UserError(
                "2KB dünyasına henüz girişiniz yapılmamış görünüyor. 2KB ile iletişime geçip aktivasyon sürecini tamamlayabilirsiniz! (2kb.com.tr)"
            )

        try:
            data = json.dumps(data)
            if company.is_encrypted_messaging:
                db_uuid = (
                    self.env["ir.config_parameter"].sudo().get_param("database.uuid")
                )
                crypter = CryptEncrypteMessage(
                    company.priv_key_2kb, company.pub_key_2kb, db_uuid
                )
                data = crypter.long_encrypte(data).decode()

            payload = {
                "json_rpc": "2.0",
                "method": "POST",
                "params": {
                    "encrypted_messaging": company.is_encrypted_messaging,
                    "payload": data,
                },
            }
            headers = {
                "Content-Type": "application/json",
                "x-auth": company.auth_key_2kb,
            }
            r = requests.post(
                self._get_url(app), json=payload, headers=headers, timeout=15
            )
            r.raise_for_status()

            response_data = r.json()
            error = response_data.get("error")
            if error:
                message = ""
                if error.get("data"):
                    message = error.get("data").get("message")
                else:
                    message = error.get("message")
                raise UserError("Error : %s" % message)

        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 500:
                _logger.exception(error)
            raise UserError(
                "API Sunucusu: "
                + _("hata kodu: (code %s) ", error.response.status_code)
            )
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise ValidationError("API Sunucusu ile bağlantı kurulamadı.")
        except Exception as e:
            _logger.exception(e)
            raise UserError(e)

        if response_data.get("result"):
            result = response_data.get("result")
            if result.get("ubl", False):
                if company.is_encrypted_messaging:
                    return crypter.long_decrypte(result.get("ubl")), False
                return result.get("ubl").encode("utf-8"), False

    def _get_url(self, app):
        raise NotImplementedError

    def _get_base_url(self, endpoint):
        ICP = self.env["ir.config_parameter"].sudo().get_param
        url = ICP("2kb.base_url", "https://api.2kb.com.tr")
        return f"{url}/{endpoint}"


class PublisherWarrantyContract(AbstractModel):
    _inherit = "publisher_warranty.contract"

    @api.model
    def _get_sys_logs(self):
        res = super()._get_sys_logs()

        try:
            msg = self._get_message()
            companies = self.env["res.company"].search([])
            vals = []
            for company in companies:
                new_msg = copy.deepcopy(msg)
                new_msg.update(
                    {
                        "auth_key_2kb": company.auth_key_2kb,
                        "vat": company.vat,
                        "company_id": company.id,
                    }
                )
                vals.append(new_msg)

            ICP = self.env["ir.config_parameter"].sudo().get_param
            url = ICP("2kb.base_url", "https://api.2kb.com.tr")
            url = url + "/publisher-warranty"

            payload = {"json_rpc": "2.0", "method": "POST", "params": {"vals": vals}}
            headers = {
                "Content-Type": "application/json",
            }
            requests.post(url, json=payload, headers=headers, timeout=30)
        except Exception:
            pass

        return res
