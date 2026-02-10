import base64
import json
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import requests
from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    kita_api_key = fields.Char(string="Kıta API Key")
    kita_api_secret = fields.Char(string="Kıta API Secret")
    kita_api_base_url = fields.Char(string="Kıta API Base URL")

    def get_kita_token(self, scope):
        """Get authentication token from Kıta API"""
        if not self.kita_api_key or not self.kita_api_secret or not self.kita_api_base_url:
            return {'error': 'API yapılandırması eksik'}

        data = {
            'username': self.kita_api_key,
            'password': self.kita_api_secret,
            'scope': scope
        }
        try:
            session = self._get_kita_api_session()
            resp = session.post(self._get_kita_token_url(), data=data, timeout=(5, 25))
        except requests.exceptions.RequestException as e:
            return {'error': "Kıta API ile bağlantı sorunu, lütfen daha sonra tekrar deneyin. %s" % e}

        if resp.status_code == 200:
            if resp.text:
                return resp.json()
            return {'success': resp.status_code}
        else:
            error_detail = self._extract_error_detail(resp)
            return {'error': error_detail}

    def _get_kita_api_session(self):
        """Create and configure requests session with retry logic"""
        session = requests.Session()
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=requests.adapters.Retry(
            total=5,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504],
        )))
        return session

    def _get_kita_token_url(self):
        """Get token endpoint URL"""
        return f"{self.kita_api_base_url.rstrip('/')}/auth/token"

    def _extract_error_detail(self, response):
        """Extract error details from API response"""
        try:
            return response.json().get('detail', 'Bilinmeyen hata oluştu! (Token Alma)')
        except Exception:
            return response.text or 'Bilinmeyen hata oluştu! (Token Alma)'

    @api.model
    def _decode_jwt_payload_kita(self, jwt_token_str):
        """Helper method to decode JWT token payload"""
        parts = jwt_token_str.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid JWT token format")

        payload_part = parts[1]
        payload_part += "=" * (-len(payload_part) % 4)

        decoded_bytes = base64.b64decode(payload_part)
        decoded_str = decoded_bytes.decode("utf-8")
        return json.loads(decoded_str)

    @api.model
    def check_kita_token_expiration(self, jwt_token_str):
        """Check if JWT token is expired or will expire in next 5 minutes"""
        try:
            payload = self._decode_jwt_payload_kita(jwt_token_str)
            expiration_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            current_time = datetime.now(timezone.utc) + relativedelta(minutes=5)

            return current_time > expiration_time
        except Exception:
            return True

    def test_kita_api_connection(self):
        """Test API connection and show result in a notification"""
        result = self.get_kita_token('test')
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
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Bağlantı Başarılı'),
                    'message': _('Kıta API ile bağlantı başarıyla kuruldu.'),
                    'type': 'success',
                    'sticky': False,
                }
            }