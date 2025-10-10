# Kıta API Services

Bu modül Kıta Yazılım API hizmetleri için API Key ve Secret bilgilerini saklamak amacıyla geliştirilmiştir.

## Amaç

Müşterilere verilen API Key ve API Secret bilgilerini Odoo Settings içerisinde basit ve güvenli bir şekilde saklamak.

## Özellikler

### Basit Yapılandırma
- Settings menüsünde tek ekranda tüm ayarlar
- API Key, Secret ve Base URL alanları
- Şifre olarak saklanan Secret alanı

### Kolay Kullanım
- Model gerektirmez
- Direkt config parameter olarak saklanır
- Diğer modüller tarafından kolay erişim

## Kurulum

1. Modülü Odoo addons dizinine kopyalayın
2. Odoo'yu yeniden başlatın
3. Apps menüsünden "Kıta API Services" modülünü yükleyin

## Kullanım

### Settings Üzerinden Yapılandırma
1. Settings > Kıta API Services menüsüne gidin
2. API Key, Secret ve Base URL bilgilerini girin
3. Kaydet butonuna tıklayın

## Diğer Modüllerle Entegrasyon

Bu modül diğer Kıta Yazılım modülleri tarafından kullanılmak üzere tasarlanmıştır:

```python
# Config parameter'lardan kimlik bilgilerini alma
api_key = self.env['ir.config_parameter'].sudo().get_param('kita_api_services.api_key')
api_secret = self.env['ir.config_parameter'].sudo().get_param('kita_api_services.api_secret')
base_url = self.env['ir.config_parameter'].sudo().get_param('kita_api_services.base_url')
```

## Saklanan Bilgiler

### Config Parameters
- `kita_api_services.api_key`: API anahtarı
- `kita_api_services.api_secret`: API gizli anahtarı
- `kita_api_services.base_url`: API base URL

## Lisans

LGPL-3.0

## Destek

Kıta Yazılım - destek@kitayazilim.com
