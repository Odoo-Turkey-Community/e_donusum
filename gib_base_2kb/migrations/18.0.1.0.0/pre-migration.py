
import logging
from odoo.upgrade import util

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = util.env(cr)

    util.remove_module(cr, 'account_invoice_currency_rate_export_2kb')
