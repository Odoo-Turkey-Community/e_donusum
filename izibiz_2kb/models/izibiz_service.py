# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import logging
import os
import base64
import zipfile
import io
import json
from lxml import etree
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from urllib3.util import Retry
import requests
from requests import Session
from requests.adapters import HTTPAdapter

import zeep
from odoo.exceptions import UserError
from odoo.tools.misc import file_path

_logger = logging.getLogger(__name__)

izibiz_clients = {}

class IzibizService:

    def __init__(self, provider):
        self.provider = provider

        self.auth_client = lambda: self._get_client("auth")
        self.fatura_client = lambda: self._get_client("e-fatura")
        self.arsiv_client = lambda: self._get_client("e-arsiv")

        if not self.provider.izibiz_jwt:
            self.auth()
        else:
            if self.is_token_expired(self.provider.izibiz_jwt):
                self.auth()

    def _get_client(self, type):
        global izibiz_clients
        env = "prod" if self.provider.prod_environment else "demo"
        key = f"{type}_{env}_{self.provider.id}"

        ws_client = izibiz_clients.get(key)
        if ws_client:
            return ws_client

        session = Session()
        if self.provider.ssl_check != 'local':
            session.verify = self.provider.ssl_check == 'true'

        retries = Retry(
            total=10,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods={'POST', 'GET'},
        )
        session.mount('https://', HTTPAdapter(max_retries=retries))
        session.mount('http://', HTTPAdapter(max_retries=retries))
        transport = zeep.transports.Transport(session=session, operation_timeout=(10, 30))
        setting = zeep.Settings(strict=False, xml_huge_tree=True, xsd_ignore_sequence_order=True)

        parent_folder = [env, f"{type}.wsdl"]
        wsdl_path_root = os.path.join(file_path("izibiz_2kb"), "data", "wsdl", *parent_folder)
        izibiz_clients[key] = zeep.Client(
            f"file://{wsdl_path_root}",
            settings=setting,
            transport=transport
        )
        return izibiz_clients[key]

    @staticmethod
    def decode_jwt(token):
        header, payload, signature = token.split('.')

        def fix_padding(base64_string):
            return base64_string + '=' * (4 - len(base64_string) % 4)

        header = base64.urlsafe_b64decode(fix_padding(header))
        payload = base64.urlsafe_b64decode(fix_padding(payload))
        return header, payload

    def is_token_expired(self, token):
        _, payload_str = IzibizService.decode_jwt(token)
        payload = json.loads(payload_str)
        exp = payload.get('exp')

        if exp is None:
            raise ValueError("Token has no expiration date (exp field)")

        expiration_time = datetime.fromtimestamp(exp, timezone.utc)
        current_time = datetime.now(timezone.utc)

        return current_time >= (expiration_time - relativedelta(hours=4))

    # -------------------------------------------------------------------------
    # Helper
    # -------------------------------------------------------------------------

    def auth(self):
        responce = self.auth_client().service.Login(
            REQUEST_HEADER=False,
            USER_NAME=self.provider.izibiz_username,
            PASSWORD=self.provider.izibiz_password,
        )
        if responce.ERROR_TYPE:
            raise UserError(responce.ERROR_TYPE.ERROR_SHORT_DES)
        self.provider.izibiz_jwt = responce.SESSION_ID

    def get_header(self):
        header_type = self.auth_client().get_type("ns2:REQUEST_HEADERType")
        return header_type(
            SESSION_ID=self.provider.izibiz_jwt,
            APPLICATION_NAME="Odoo-2kb",
            CHANNEL_NAME="2kb",
        )

    # -------------------------------------------------------------------------
    # Account API
    # -------------------------------------------------------------------------
    def check_user(self, vkn, unit="PK"):
        """
        'ERROR_TYPE': None,
        'USER': [
            {
                'IDENTIFIER': '4840847211',
                'ALIAS': 'urn:mail:defaultpk@izibiz.com.tr',
                'TITLE': 'İZİBİZ BİLİŞİM TEKNOLOJİLERİ ANONİM ŞİRKETİ',
                'TYPE': 'OZEL',(Firmanın GİB sisteminde tanımlı tipi. OZEL veya KAMU olabilir.)
                'REGISTER_TIME': '2016-12-15T17:07:17',
                'UNIT': 'PK',
                'ALIAS_CREATION_TIME': '2017-01-11T16:32:16',
                'ACCOUNT_TYPE': 'OZELENTEGRASYON',
                'DELETED': 'N',
                'ALIAS_DELETION_TIME': None,
                'DOCUMENT_TYPE': 'INVOICE'
            }
        ]
        """
        success = error = False
        try:
            responce = self.auth_client().service.CheckUser(
                self.get_header(), USER={"IDENTIFIER": vkn, "UNIT": unit}
            )
        except requests.exceptions.ConnectTimeout as e:
            return {
                "success": success,
                "error": "Connection Error!\n" + str(e),
            }

        if not responce.ERROR_TYPE:
            success = True
        else:
            if responce.ERROR_TYPE.ERROR_CODE in (10002, 10004, 1006):
                # login zaman aşımı
                self.auth()
                return self.check_user(vkn)
            else:
                error = responce.ERROR_TYPE.ERROR_SHORT_DES

            _logger.warning(f"izibiz e-fatura(check_user) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

        return {
            "success": success,
            "error": error,
            "result": responce.USER if success else False,
        }

    def get_gib_user_list(
        self,
        document_type="ALL",
        alias_type="PK",
        register_time_start=None,
        alias_modify_date=None,
    ):
        """
        E-Fatura ve E-İrsaliye sistemine kayıtlı firmalara ait GB/PK etiketlerinin sıkıştırılmış olarak istenilen tipte dönüldüğü servistir.
        params:
            DOCUMENT_TYPE: ALL, INVOICE, DESPATCHADVICE
            ALIAS_TYPE: ALL, PK
            ALIAS_MODIFY_DATE: 2019-12-01  YYYY-AA-GGTSS:DD:SS
            REGISTER_TIME_START: 2019-12-01  YYYY-AA-GGTSS:DD:SS

        """
        success = error = False
        try:
            responce = self.auth_client().service.GetGibUserList(
                REQUEST_HEADER={
                    "SESSION_ID": self.provider.izibiz_jwt,
                    "APPLICATION_NAME": "Odoo-2kb",
                },
                TYPE="XML",
                DOCUMENT_TYPE=document_type,
                ALIAS_TYPE=alias_type,
                REGISTER_TIME_START=register_time_start,
                ALIAS_MODIFY_DATE=alias_modify_date,
            )
        except requests.exceptions.ConnectTimeout as e:
            return {
                "success": success,
                "error": "Connection Error!\n" + str(e),
            }

        if not responce.ERROR_TYPE:
            success = True
            z = zipfile.ZipFile(io.BytesIO(responce.CONTENT._value_1))
            xml = z.read(z.infolist()[0])
            xml_str = xml.decode()
            clean_xml = xml_str.replace('xmlns=""', "")
            clean_xml = clean_xml.replace('xmlns="http://schemas.i2i.com/ei/wsdl"', "")
            xml_tree = etree.fromstring(clean_xml)
        else:
            if responce.ERROR_TYPE.ERROR_CODE in (10002, 10004):
                # login zaman aşımı
                self.auth()
                return self.get_gib_user_list(
                    document_type,
                    alias_type,
                    register_time_start,
                    alias_modify_date,
                )
            else:
                error = responce.ERROR_TYPE.ERROR_SHORT_DES

            _logger.warning(f"izibiz e-fatura(get_gib_user_list) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

        return {
            "success": success,
            "error": error,
            "result": xml_tree if success else False,
        }

    # -------------------------------------------------------------------------
    # E-Invoice API
    # -------------------------------------------------------------------------

    def load_invoice(self, move_content, retry=True):
        blocking_level = error = success = False
        responce = self.fatura_client().service.LoadInvoice(
            REQUEST_HEADER={
                "SESSION_ID": self.provider.izibiz_jwt,
                "APPLICATION_NAME": "Odoo-2kb",
                "COMPRESSED": "N",
            },
            INVOICE={"CONTENT": move_content},
        )

        if not responce.ERROR_TYPE:
            success = True
        else:
            if responce.ERROR_TYPE.ERROR_CODE in (10009, 10017):
                # tekrarlı gönderin
                success = True
                blocking_level = "info"
            elif responce.ERROR_TYPE.ERROR_CODE in (10002, 10004, 10006) and retry:
                # login zaman aşımı
                self.auth()
                return self.load_invoice(move_content, retry=False)
            elif responce.ERROR_TYPE.ERROR_CODE in (-1, 10001):
                # bilinmeyen hata
                error = responce.ERROR_TYPE.ERROR_SHORT_DES
                blocking_level = "info"
            else:
                error = responce.ERROR_TYPE.ERROR_SHORT_DES
                blocking_level = "error"

            _logger.warning(f"izibiz e-fatura(load_invoice) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")
        return {
            "success": success,
            "error": error,
            "blocking_level": blocking_level,
        }

    def send_invoice(self, move_content, GB, PK, retry=True):
        """SendInvoice metodu ile fatura gönderimi yapılacak."""
        blocking_level = error = success = False
        responce = self.fatura_client().service.SendInvoice(
            REQUEST_HEADER={
                "SESSION_ID": self.provider.izibiz_jwt,
                "COMPRESSED": "N",
            },
            SENDER={"alias": GB},
            RECEIVER={"alias": PK},
            INVOICE={"CONTENT": move_content},
        )

        if not responce.ERROR_TYPE:
            success = True
        else:
            _logger.warning(f"izibiz e-fatura(send_invoice) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

            if responce.ERROR_TYPE.ERROR_CODE in (10009, 10017):
                # tekrarlı gönderin
                success = True
                blocking_level = "info"
            elif responce.ERROR_TYPE.ERROR_CODE in (10002, 10004, 10006) and retry:
                # login zaman aşımı
                self.auth()
                return self.send_invoice(move_content, GB, PK, retry=False)
            elif responce.ERROR_TYPE.ERROR_CODE in (-1, 10001):
                # bilinmryen hata
                error = responce.ERROR_TYPE.ERROR_SHORT_DES
                blocking_level = "info"
            else:
                error = (
                    responce.ERROR_TYPE.ERROR_SHORT_DES
                    + " Kod: "
                    + str(responce.ERROR_TYPE.ERROR_CODE)
                )
                blocking_level = "error"

        return {
            "success": success,
            "error": error,
            "blocking_level": blocking_level,
        }

    def get_invoice_status(self, id=None, uuid=None, retry=True):
        """E-Fatura sisteminde bulunan bir veya birden fazla taslak,
        gelen ve giden faturaların durumunu sorgulamayı sağlayan servistir.
            :params id string:
                Durumu sorgulanacak faturanın 16 hane fatura numarası. örnek: FYA2018000000001 Eğer UUID elemanı gönderilmezse zorunludur.
            :params id uuid:
                Durumu sorgulanacak faturanın GUID formatında Evrensel Tekil Tanımlama Numarası. Eğer ID elemanı gönderilmezse zorunludur.
            :return dict:
            {
                "success": True | False,
                "error": error,
                "result": {
                    'HEADER': None,
                    'CONTENT': None,
                    'STATUS': 'RECEIVE - WAIT_APPLICATION_RESPONSE',
                    'STATUS_DESCRIPTION': 'WAIT_APPLICATION_RESPONSE',
                    'GIB_STATUS_CODE': -1,
                    'GIB_STATUS_DESCRIPTION': None,
                    'RESPONSE_CODE': None,
                    'RESPONSE_DESCRIPTION': None,
                    'CDATE': datetime.datetime(2024, 5, 3, 8, 47, 58, tzinfo=<FixedOffset '+03:00'>),
                    'ENVELOPE_IDENTIFIER': 'd3adb140-c151-44ce-8596-faaa278d2cdb',
                    'GTB_REFNO': None, Gümrük Sistemine alınan ihracat faturaları için, Gümrük ve Ticaret Bakanlığı tarafından üretilen 23 haneli bir referans numarasıdır.
                    'GTB_GCB_TESCILNO': Gümrük İdaresi fiili ihracatı tamamlanan eşyanın kabul uygulama yanıtı ile ilgilisine dönülen Gümrük Çıkış Belgesi (GÇB) tescil numarasıdır. ,
                    'GTB_FIILI_IHRACAT_TARIHI': Gümrük İdaresi tarafından fiili ihracatı tamamlanan ihracat faturaları için döndüğü fiili ihraç tarihi bilgisidir. Gümrük İdaresi bu bilgiyi fiili ihracat (intaç) gerçekleştiğinde dönecektir.,
                    'STATUS_CODE': '132',
                    'DIRECTION': 'IN',
                    'WEB_KEY': 'https://portaltest.izibiz.com.tr/belge/goruntule?ZG9jdW1lbnRUeXBlPUVJTlZPSUNFX0VYVEVSTkFMJndlYlZhbGlkYXRpb25LZXk9ODA5OGMzMWMtZWU5MS00ZDY4LTkzZGMtOWUwYjdkMzJlYmU1JnZpZXdUeXBlPVBERg==',
                    'ID': 'XFX2024000000147',
                    'UUID': '6bdb7993-975d-4712-9e8c-39842d24a123',
                    'LIST_ID': None
                },
            }
        """
        success = error = False
        responce = self.fatura_client().service.GetInvoiceStatus(
            REQUEST_HEADER={
                "SESSION_ID": self.provider.izibiz_jwt,
                "APPLICATION_NAME": "Odoo-2kb",
            },
            INVOICE={"ID": id, "UUID": uuid},
        )

        if not responce.ERROR_TYPE:
            success = True
        else:
            _logger.warning(f"izibiz e-fatura(get_invoice_status) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

            if responce.ERROR_TYPE.ERROR_CODE in (10002, 10004, 10006) and retry:
                # login zaman aşımı
                self.auth()
                return self.get_invoice_status(id, uuid, retry=False)
            else:
                error = responce.ERROR_TYPE.ERROR_SHORT_DES

        return {
            "success": success,
            "error": error,
            "result": responce.INVOICE_STATUS if success else False,
        }

    def get_invoice(
        self,
        header_only="Y",
        **kw,
    ):
        """
        E-Fatura sisteminden giden imzalı faturaları veya gelen faturaları muhasebe paketine çekmek için kullanılır.
        Fatura özet bilgilerini veya fatura özet bilgileri ile beraber XML içeriğini de çekmek için kullanılabilir.
        Entegrasyon yapan iş ortaklarımızdan yeni gelen bütün faturaları içerikleri (XML) beraber müşteri ortamına çekilmesini tavsiye ediyoruz.
        İçerik ile beraber en fazla 100 fatura çekilebilir.
        Fatura özet bilgileri ile en fazla 25000 adet fatura dönülmektedir.
        Alıcı tarafından zamanlanmış fatura çekme özelliği eklenecekse en fazla 15 dakika aralığında olmalıdır.
        SEARCH_KEY:
            LIMIT 	 	    (int)Kaç fatura okunmak istendiği. Eğer eleman gönderilmezse 10 adet fatura, fatura içerikleri (XML) ile beraber en fazla 100 adet fatura, sadece fatura başlıklarını çekildiğindeise en fazla 25.000 adet fatura dönülür.
            FROM 	 	    Gönderici firma gönderici birim (GB) etiketine göre çekmek için kullanılabilir. Örneğin birden fazla GB etiketi olan bir firmanın sadece muhasebe departmanından gelen faturaları okumak için kullanılabilir. format: urn:mail:muhasebegb@firma.com
            TO 	 	        Birden fazla Posta Kutusu (PK) etiketi olan bir firmanın sadece bir PK adresine gelen faturaları çekmek için kullanılabilir. Eğer etiket gönderilmez ise kullanıcının yetkisine bağlı olarak bütün faturalar dönülür. format: urn:mail:muhasebepk@firma.com
            ID 	 	        Fatura numarası ile fatura okumak için kullanılabilir. format: FYA2018000000001
            UUID 	 	    Evrensel Tekil Tanımlama Numarası (ETTN) ile fatura okumak için kullanılabilir. GUID formatında
            DATE_TYPE 	 	Belirli tarih aralığında fatura çekmek istendiğinde belirlenen tarih tipidir. CREATE değeri gönderilirse fatura oluşturulma tarihine göre getirilir, boş veya ISSUE değeri gönderilirse fatura tarihine göre getirilmektedir.
            START_DATE 	 	Belirli tarih aralığında fatura çekmek istendiğinde dönem başlangıç tarihi format: YYYY-MM-DD
            END_DATE 	 	Belirli tarih aralığında fatura çekmek istendiğinde dönem bitiş tarihi format: YYYY-MM-DD
            READ_INCLUDED 	(Boolean)Fatura okurken daha önce okunmuş faturaları dönüşe dahil edilip edilmeyeceğini belirler. true değeri gönderilirse fatura daha önce okunmuş olsa bile yanıta eklenir. Gönderilmezse veya false gönderilirse sadece yeni gelen faturalar dönülür. Değerler: true/false
            DRAFT_FLAG 	 	Taslak faturaları sonuca eklenmesi için kullanılan parametredir. Y değeri gönderilirse taslak faturalar diğer kriterlere uyan faturalarla beraber sonuca eklenir. Parametre gönderilmezse veya N gönderilirse taslak faturalar sonuca eklenmez. Değerler: Y/N
            DIRECTION 	 	Belge yönü. Gelen veya Giden faturaları çekmek için kullanılabilir. Gelen faturaları çekmek için IN, giden faturaları çekmek için OUT değeri gönderilebilir. Varsayılan değer IN olduğu için eğer parametre gönderilmezse sadece gelen faturalar dönülecektir. Gönderilebilecek değerler: IN, OUT
        """

        success = error = False
        try:
            responce = self.fatura_client().service.GetInvoice(
                REQUEST_HEADER={
                    "SESSION_ID": self.provider.izibiz_jwt,
                    "APPLICATION_NAME": "Odoo-2kb",
                    "COMPRESSED": "N",
                },
                INVOICE_SEARCH_KEY={
                    **kw,
                },
                HEADER_ONLY=header_only,
            )
        except requests.exceptions.ConnectTimeout as e:
            return {
                "success": success,
                "error": "Connection Error!\n" + str(e),
            }

        if not responce.ERROR_TYPE:
            success = True
        else:
            _logger.warning(f"izibiz e-fatura(get_invoice) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

            if responce.ERROR_TYPE.ERROR_CODE in (10002,):
                # login zaman aşımı
                self.auth()
                return self.get_invoice(header_only, **kw)
            else:
                error = responce.ERROR_TYPE.ERROR_SHORT_DES


        return {
            "success": success,
            "error": error,
            "result": responce.INVOICE if success else False,
        }

    def mark_invoice(self, uuids, value="READ"):
        """MarkInvoice metodu ile başarılı şekilde teslim alınan faturalar izibiz sistemlerinde okundu olarak işaretlenir.
        Böylece bir sonra ki getinvoice servisi çağrılınca dönülmez.
        Başarı ile alındıysa READ gönderilmeli. Daha önce alındı olarak işaretlenen bir faturayı tekrar çekmeden önce UNREAD olarak gönderilebilir.
        """

        success = error = False
        try:
            responce = self.fatura_client().service.MarkInvoice(
                REQUEST_HEADER={
                    "SESSION_ID": self.provider.izibiz_jwt,
                    "APPLICATION_NAME": "Odoo-2kb",
                },
                MARK={"INVOICE": [{"UUID": uuid} for uuid in uuids], "value": value},
            )
        except requests.exceptions.ConnectTimeout as e:
            return {
                "success": success,
                "error": "Connection Error!\n" + str(e),
            }

        if not responce.ERROR_TYPE:
            success = True
        else:
            _logger.warning(f"izibiz e-fatura(mark_invoice) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

            if responce.ERROR_TYPE.ERROR_CODE in (10002,):
                # login zaman aşımı
                self.auth()
                return self.mark_invoice(uuids, value)
            else:
                error = responce.ERROR_TYPE.ERROR_SHORT_DES

        return {
            "success": success,
            "error": error,
        }

    def get_invoice_status_all(self, uuids):
        """E-Fatura sisteminde bulunan bir veya birden fazla taslak, gelen ve giden faturaların durumunu sorgulamayı sağlayan servistir."""

        success = error = False
        try:
            responce = self.fatura_client().service.GetInvoiceStatusAll(
                REQUEST_HEADER={
                    "SESSION_ID": self.provider.izibiz_jwt,
                    "APPLICATION_NAME": "Odoo-2kb",
                },
                UUID=uuids,
            )
        except requests.exceptions.ConnectTimeout as e:
            return {
                "success": success,
                "error": "Connection Error!\n" + str(e),
            }

        if not responce.ERROR_TYPE:
            success = True
        else:
            _logger.warning(f"izibiz e-fatura(get_invoice_status_all) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

            if responce.ERROR_TYPE.ERROR_CODE in (10002,):
                # login zaman aşımı
                self.auth()
                return self.get_invoice_status_all(uuids)
            else:
                error = responce.ERROR_TYPE.ERROR_SHORT_DES

        return {
            "success": success,
            "error": error,
            "result": responce.INVOICE_STATUS if success else False,
        }

    def send_invoice_response_with_server_sign(self, uuid, status, desc=None):
        """Uygulama Yanıtı Gönderme. Servis çoklu ama biz tekil gönderiyoruz!!

        bazı servis parametreleri:
            STATUS: Faturaya verilecek yanıt. KABUL veya RED değeri alabilir.
            DESCRIPTION: Ret edilen faturalar için Red Sebebi bu alana yazılabilir.

        bazı hatalar:
            -Daha önce yanıtlanmış bir fatura için tekrar yanıt gönderilemez! Fatura UUID:xxxxxxx,
            -Fatura ID : FYA201800000001 sistemde bulunamadı!,
            -Uygulama yanıtı 8 gün geciktiği için cevap gönderilemez( CDATE + 8 )
            -Fatura durumu yanıtlama için uygun olmadıgından işlem sonlandı! Fatura UUID:XXX-XXX-, STATUS:XXXXX-XXXXX

        """
        success = error = False
        try:
            responce = self.fatura_client().service.SendInvoiceResponseWithServerSign(
                REQUEST_HEADER={
                    "SESSION_ID": self.provider.izibiz_jwt,
                    "APPLICATION_NAME": "Odoo-2kb",
                },
                STATUS=status,
                INVOICE={"UUID": uuid},
                DESCRIPTION=desc,
            )
        except requests.exceptions.ConnectTimeout as e:
            return {
                "success": success,
                "error": "Connection Error!\n" + str(e),
            }

        if not responce.ERROR_TYPE:
            success = True
        else:
            _logger.warning(f"izibiz e-fatura(send_invoice_response_with_server_sign) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

            if responce.ERROR_TYPE.ERROR_CODE in (10002,):
                # login zaman aşımı
                self.auth()
                return self.send_invoice_response_with_server_sign(uuid, status, desc)
            else:
                error = responce.ERROR_TYPE.ERROR_SHORT_DES

        return {
            "success": success,
            "error": error,
        }

    def get_invoice_with_type(self, header_only="N", **kw):
        """
        Fatura Görsel Okuma (GetInvoiceWithType)
        örnek parametre dizilimi UUID=invoice, READ_INCLUDED="Y", TYPE="PDF", DIRECTION="IN", header_only="N"
        READ_INCLUDED'a dikkaet et
        """
        success = error = False
        try:
            responce = self.fatura_client().service.GetInvoiceWithType(
                REQUEST_HEADER={
                    "SESSION_ID": self.provider.izibiz_jwt,
                    "APPLICATION_NAME": "Odoo-2kb",
                },
                INVOICE_SEARCH_KEY={
                    **kw,
                },
                HEADER_ONLY=header_only,
            )
        except requests.exceptions.ConnectTimeout as e:
            return {
                "success": success,
                "error": "Connection Error!\n" + str(e),
            }

        content = b""
        if not responce.ERROR_TYPE:
            success = True
            if responce.INVOICE:
                z = zipfile.ZipFile(io.BytesIO(responce.INVOICE[0].CONTENT._value_1))
                content = z.read(z.infolist()[0])
        else:
            _logger.warning(f"izibiz e-fatura(get_invoice_with_type) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

            if responce.ERROR_TYPE.ERROR_CODE in (10002,):
                # login zaman aşımı
                self.auth()
                return self.get_invoice_with_type(header_only, **kw)
            else:
                error = responce.ERROR_TYPE.ERROR_SHORT_DES

        return {
            "success": success,
            "error": error,
            "content": content if success else False,
        }

    # -------------------------------------------------------------------------
    # E-Archive API
    # -------------------------------------------------------------------------
    def write_to_archive_extended(
        self, move_content, atype="NORMAL", sub_status="NEW", retry=True
    ):
        """
        *E-Fatura mükellefi olmayan firmalara veya nihai tüketicilere düzenlenen faturaların özel entegratör sistemine gönderilmesini sağlayan servistir.
        *Bir istek içerisinde birden fazla fatura göndermek için ArchiveInvoiceExtendedContent elemanı çoklanmalıdır.
        *Internet üzerinde yapılan satış için düzenlenen faturalarında e-arşiv tipi INTERNET olmak zorundadır. Diğer faturalar için NORMAL olacaktır.
        *Eğer E-Arşiv sisteminde müşterinin e-posta gönderme hizmeti yoksa ve e-posta gönderme seçeneği seçilmişse işlem hata alacaktır.
            Bu durumda özel entegratör ile iletişime geçerek e-posta gönderim hizmetini aktiflemesi talep edilmelidir.
            Eğer e-posta gönderimi farklı kanallardan yapılacaksa e-posta gönderim parametresini N olarak gönderiniz.

        """
        blocking_level = error = success = False
        try:
            responce = self.arsiv_client().service.WriteToArchiveExtended(
                REQUEST_HEADER={
                    "SESSION_ID": self.provider.izibiz_jwt,
                    "APPLICATION_NAME": "Odoo-2kb",
                    "COMPRESSED": "N",
                },
                ArchiveInvoiceExtendedContent={
                    "INVOICE_PROPERTIES": [
                        {
                            "EARSIV_FLAG": "Y",
                            "EARSIV_PROPERTIES": {
                                "EARSIV_TYPE": atype,  # NORMAL, INTERNET
                                "SUB_STATUS": sub_status,  # DRAFT, NEW
                                "EARSIV_EMAIL_FLAG": "N",
                                "EARSIV_EMAIL": None,
                            },
                            "PDF_PROPERTIES": {},
                            "ARCHIVE_NOTE": None,
                            "INVOICE_CONTENT": move_content,
                        }
                    ]
                },
            )
        except requests.exceptions.ConnectTimeout as e:
            return {
                "success": success,
                "error": "Connection Error!\n" + str(e),
                "blocking_level": "info",
            }

        if not responce.ERROR_TYPE:
            success = True
        else:
            _logger.warning(f"izibiz e-fatura(write_to_archive_extended) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

            if responce.ERROR_TYPE.ERROR_CODE in (10009, 10017):
                # tekrarlı gönderin
                success = True
                blocking_level = "info"
            elif responce.ERROR_TYPE.ERROR_CODE in (10002, 10004, 10006) and retry:
                # login zaman aşımı
                self.auth()
                return self.write_to_archive_extended(
                    move_content, atype, sub_status, retry=False
                )
            elif responce.ERROR_TYPE.ERROR_CODE in (-1, 10001):
                # bilinmryen hata
                error = responce.ERROR_TYPE.ERROR_SHORT_DES
                blocking_level = "info"
            else:
                error = (
                    responce.ERROR_TYPE.ERROR_SHORT_DES
                    + " Kod: "
                    + str(responce.ERROR_TYPE.ERROR_CODE)
                )
                blocking_level = "error"

        return {
            "success": success,
            "error": error,
            "blocking_level": blocking_level,
        }

    def read_from_archive(self, uuid, format="XML"):
        """
        Özel entegratör sistemine gönderilen e-arşiv faturalarının farklı formatlarda (XML,HTML,PDF) okumasını sağlayan servistir.

        """
        success = error = False
        try:
            responce = self.arsiv_client().service.ReadFromArchive(
                REQUEST_HEADER={
                    "SESSION_ID": self.provider.izibiz_jwt,
                    "APPLICATION_NAME": "Odoo-2kb",
                    "COMPRESSED": "N",
                },
                INVOICEID=uuid,
                PORTAL_DIRECTION="OUT",
                PROFILE=format,  # PDF, HTML, XML
            )
        except requests.exceptions.ConnectTimeout as e:
            return {
                "success": success,
                "error": "Connection Error!\n" + str(e),
            }

        if not responce.ERROR_TYPE:
            success = True
        else:
            _logger.warning(f"izibiz e-fatura(read_from_archive) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

            if responce.ERROR_TYPE.ERROR_CODE in (10002,):
                # login zaman aşımı
                self.auth()
                return self.read_from_archive(uuid, format)
            else:
                error = responce.ERROR_TYPE.ERROR_SHORT_DES

        return {
            "success": success,
            "error": error,
            "result": responce.INVOICE[0]._value_1 if success else False,
        }

    def get_earchive_status(self, uuids):
        """
        Özel entegratör platformuna gönderilen bir veya birden çok faturanın durumunu sorgulamayı sağlayan servistir.
        [{
            'INVOICE_ID': 'AEX2024000000006',
            'PROFILE': 'EARSIVFATURA',
            'UUID': '15e6544f-d8a1-4d2a-b4c2-d568c82c60b5',
            'INVOICE_DATE': '09-05-2024',
            'STATUS': '130',
            'STATUS_DESC': 'RAPORLANDI',
            'EMAIL_STATUS': None,
            'EMAIL_STATUS_DESC': None,
            'REPORT_ID': 107452,
            'WEB_KEY': 'https://portaltest.izibiz.com.tr/earchive/view-earchive/view-pdf-earchive.xhtml?webValidationKey=380af57bb4c3c357829293a1f77adb9c4c36479a9a8166474d528d380e7309d3de087e68b5b81510&viewType=PDF'
        }]
        100 	KUYRUĞA EKLENDİ
        105 	TASLAK OLARAK EKLENDİ
        110 	İŞLENİYOR
        120 	RAPORLANACAK
        130 	RAPORLANDI
        150 	RAPORLANMADAN İPTAL EDİLDİ. RAPORLANMAYACAK.
        200 	FATURA ID BULUNAMADI
        """
        success = error = False
        responce = self.arsiv_client().service.GetEArchiveInvoiceStatus(
            REQUEST_HEADER={
                "SESSION_ID": self.provider.izibiz_jwt,
                "APPLICATION_NAME": "Odoo-2kb",
            },
            UUID=uuids,
        )

        if not responce.ERROR_TYPE:
            success = True
        else:
            _logger.warning(f"izibiz e-fatura(get_earchive_status) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

            if responce.ERROR_TYPE.ERROR_CODE in (10002,):
                # login zaman aşımı
                self.auth()
                return self.get_earchive_status(uuids)
            else:
                error = responce.ERROR_TYPE.ERROR_SHORT_DES


        return {
            "success": success,
            "error": error,
            "result": responce.INVOICE if success else False,
        }

    def cancel_earchive_invoice(self, uuids):
        """
        E-Arşiv Fatura İptal
        Servis hataları uuid bazlı dönmüyor.
        """
        success = error = False
        responce = self.arsiv_client().service.CancelEArchiveInvoice(
            REQUEST_HEADER={
                "SESSION_ID": self.provider.izibiz_jwt,
                "APPLICATION_NAME": "Odoo-2kb",
            },
            CancelEArsivInvoiceContent=[{"FATURA_UUID": uuid} for uuid in uuids],
        )

        if not responce.ERROR_TYPE:
            success = True
        else:
            _logger.warning(f"izibiz e-fatura(cancel_earchive_invoice) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

            if responce.ERROR_TYPE.ERROR_CODE in (10002,):
                # login zaman aşımı
                self.auth()
                return self.cancel_earchive_invoice(uuids)
            if responce.ERROR_TYPE.ERROR_CODE in (10020,):
                # tekrarlı gönderin
                success = True
            else:
                error = (
                    responce.ERROR_TYPE.ERROR_SHORT_DES
                    + " Kod: "
                    + str(responce.ERROR_TYPE.ERROR_CODE)
                )

        return {
            "success": success,
            "error": error,
        }

    def get_earchive_report(self, period, flag=None):
        """
        E-Arşiv Rapor Listesini Çekme
        """

        success = error = False
        try:
            responce = self.arsiv_client().service.GetEArchiveReport(
                REQUEST_HEADER={
                    "SESSION_ID": self.provider.izibiz_jwt,
                    "APPLICATION_NAME": "Odoo-2kb",
                },
                REPORT_PERIOD=period,  # Rapor listesinin alınmak istenilen dönem bilgisi. Örnek: Mayıs 2018 dönemi için 201805
                REPORT_STATUS_FLAG=flag,  # Rapor durumunun sonuca eklenmesi isteniyorsa Y, değilse N değeri gönderilmelidir.
            )
        except requests.exceptions.ConnectTimeout as e:
            return {
                "success": success,
                "error": "Connection Error!\n" + str(e),
            }

        if not responce.ERROR_TYPE:
            success = True
        else:
            _logger.warning(f"izibiz e-fatura(get_earchive_report) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

            if responce.ERROR_TYPE.ERROR_CODE in (10002,):
                # login zaman aşımı
                self.auth()
                return self.get_earchive_report(period, flag)
            else:
                error = responce.ERROR_TYPE.ERROR_SHORT_DES

        return {
            "success": success,
            "error": error,
        }

    def read_earchive_report(self, report_id):
        """
        Mükellef için GİB'e gönderilen raporun imzalı XML dosyasını okumayı sağlayan servistir.
        """
        success = error = False
        try:
            responce = self.arsiv_client().service.ReadEArchiveReport(
                REQUEST_HEADER={
                    "SESSION_ID": self.provider.izibiz_jwt,
                    "APPLICATION_NAME": "Odoo-2kb",
                },
                RAPOR_NO=report_id,  # Detay/içeriği çekilecek raporun IDsi. Rapor IDsine GetEArchiveReport servisini kullanarak erişebilirsiniz.
            )
        except requests.exceptions.ConnectTimeout as e:
            return {
                "success": success,
                "error": "Connection Error!\n" + str(e),
            }

        if not responce.ERROR_TYPE:
            success = True
            # iç-içe zipli dosya
            z = zipfile.ZipFile(io.BytesIO(responce.EARCHIVEREPORT[0]._value_1))
            z2 = zipfile.ZipFile(io.BytesIO(z.read(z.infolist()[0])))
            xml = z2.read(z2.infolist()[0])
        else:
            _logger.warning(f"izibiz e-fatura(read_earchive_report) uyarısı \n{responce.ERROR_TYPE.ERROR_CODE}:{responce.ERROR_TYPE.ERROR_SHORT_DES}")

            if responce.ERROR_TYPE.ERROR_CODE in (10002,):
                # login zaman aşımı
                self.auth()
                return self.read_earchive_report(report_id)
            else:
                error = responce.ERROR_TYPE.ERROR_SHORT_DES

        return {"success": success, "error": error, "result": xml if success else False}
