# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import requests
import json

from odoo import models, release, fields, _
from odoo.exceptions import ValidationError, AccessError
from odoo.addons.activation_2kb.tools.crypt_message import CryptEncrypteMessage


class ResCompany(models.Model):
    _inherit = 'res.company'

    auth_key_2kb = fields.Char("Auth Key")
    priv_key_2kb = fields.Text("Private Key")
    pub_key_2kb = fields.Text("Certificate")
    is_encrypted_messaging = fields.Boolean('Encrypted Msg.', default=True)

    def action_deactivation(self):
        self.ensure_one()
        self.write({
            'priv_key_2kb': False,
            'pub_key_2kb': False
        })

    def action_activation(self):
        self.ensure_one()

        assert self.auth_key_2kb, "auth_key variable must not be empty."

        headers = {
            'Content-Type': 'application/json',
            'x-auth': self.auth_key_2kb
        }
        payload = {
            "json_rpc": "2.0",
            "method": "POST",
            "params": {
                "db_name": self.env.cr.dbname,
                "version": release.version,
                "db_uuid": self.env["ir.config_parameter"].sudo().get_param("database.uuid")
            }
        }

        ICP = self.env["ir.config_parameter"].sudo().get_param
        url = ICP("2kb.base_url", "https://api.2kb.com.tr")
        url = f"{url}/saas/activation"
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            raise AccessError(_("Please contact the support team. Error Code: 404"))

        response_data = response.json()
        if response_data.get('result'):
            result = json.loads(response_data.get('result'))
            self.write({
                'priv_key_2kb': result.get('priv'),
                'pub_key_2kb': result.get('pub')
            })
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "type": "success",
                    "message": _("Welcome to the world of 2KB."),
                    "next": {"type": "ir.actions.act_window_close"},
                },
            }
        else:
            error = response_data.get('error')
            message = ''
            if error.get('data'):
                message = error.get('data').get('message')
            else:
                message = error.get('message')
            raise ValidationError("Error : %s" % message)

    def action_test_message(self):
        val = _("Welcome to the world of 2KB.")
        try:
            db_uuid = self.env["ir.config_parameter"].sudo().get_param("database.uuid")
            crypter = CryptEncrypteMessage(self.priv_key_2kb, self.pub_key_2kb, db_uuid)
        except Exception as exc:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "type": "warning",
                    "message": _("Certificate Password Incorrect.\n Check the Database UUID.\n %s") % exc,
                    "next": {"type": "ir.actions.act_window_close"},
                }
            }
        data = crypter.encrypte(val)

        headers = {
            'Content-Type': 'application/json',
            'x-auth': self.auth_key_2kb
        }
        payload = {
            "json_rpc": "2.0",
            "method": "POST",
            "params": {
                "data": data.decode('utf-8')
            }
        }
        ICP = self.env["ir.config_parameter"].sudo().get_param
        url = ICP("2kb.base_url", "https://api.2kb.com.tr")
        url = f"{url}/saas/test_message"
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response_data = response.json()
        if response_data.get('result'):
            result = json.loads(response_data.get('result'))
            if result.get("data", False) == val:
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "type": "success",
                        "message": "%s" % result.get("data", 'Error'),
                        "next": {"type": "ir.actions.act_window_close"},
                    },
                }
        else:
            error = response_data.get('error')
            message = ''
            if error.get('data'):
                message = error.get('data').get('message')
            else:
                message = error.get('message')
            raise ValidationError("Error : %s" % message)
