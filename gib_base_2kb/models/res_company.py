from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ResCompany(models.Model):
    _inherit = 'res.company'

    gib_ubl_gen = fields.Char(string="GIB UBL Token")

    def get_ubl_service_name(self):
        return "ubl_gen_free"

    def get_ubl_tr_token(self):
        self.ensure_one()
        if not self.gib_ubl_gen or self.check_kita_token_expiration(self.gib_ubl_gen):
            result = self.get_kita_token(self.get_ubl_service_name())
            if result.get('error'):
                raise ValidationError(result.get('error'))
            self.sudo().gib_ubl_gen = result.get('access_token')

        return self.gib_ubl_gen

    def invalidate_ubl_tr_token(self):
        for rec in self:
            rec.sudo().gib_ubl_gen = False

    def test_kita_api_ubl_connection(self):
        """Test API connection and show result in a notification, ensure that your ip is allowed in GIB API"""
        result = self.get_kita_token(self.get_ubl_service_name())
        if result.get('error'):
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Bağlantı Hatası'),
                    'message': result.get('error', _('Bilinmeyen bir hata oluştu.')),
                    'type': 'danger',
                    'sticky': False,
                }
            }
        res = self._decode_jwt_payload_kita(result.get('access_token'))
        service = list(filter(lambda s: s.get('code') == self.get_ubl_service_name(), res.get('services', [])))
        if service:
            self.sudo().gib_ubl_gen = result.get('access_token')
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Servis Hatası'),
                    'message': _('GIB UBL Servisine erişim yetkiniz bulunmamaktadır.'),
                    'type': 'danger',
                    'sticky': False,
                }
            }