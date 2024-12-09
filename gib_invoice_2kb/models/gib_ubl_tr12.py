# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

from odoo import models, _
from odoo.tools import float_repr
from odoo.exceptions import ValidationError
from odoo.tools import html2plaintext


class GibUblTR12(models.AbstractModel):
    _inherit = "gib.ubl.tr12"

    def _validate_taxes(self, invoice):
        """Validate the structure of the tax repartition lines (invalid structure could lead to unexpected results)"""
        for tax in invoice.invoice_line_ids.tax_ids:
            try:
                tax._validate_repartition_lines()
            except ValidationError as e:
                error_msg = _("Tax '%s' is invalid: %s", tax.name, e.args[0])
                raise ValidationError(error_msg)

    def _export_invoice_filename(self, invoice):
        return f"{invoice.gib_invoice_name}-{invoice.gib_uuid}.xml"

    def _get_additional_document_reference_vals(self, invoice):
        res = []
        # tasarım şablonu
        provider_name = invoice.gib_provider_id.provider
        template = invoice.sudo().gib_template_id
        if template:
            res.append(
                {
                    "id": template.checksum,
                    "issue_date": self.format_date(invoice.invoice_date),
                    "document_type": "XSLT",
                    "external_reference_uri": False,
                    "binary_object_vals": {
                        "filename": "%s.xslt" % template.store_fname,
                        "mime_code": "application/xml",
                        "attachment": template.with_context(
                            bin_size=False
                        ).datas.decode("utf-8"),
                    },
                }
            )

        res.append(
            {
                "id": invoice.name,
                "issue_date": self.format_date(invoice.invoice_date),
                "document_type_code": "odoo",
            }
        )

        if invoice.gib_profile_id == self.env.ref(
            "gib_invoice_2kb.profile_id-EARSIVFATURA"
        ):
            if provider_name == "nes":
                res.append(
                    {
                        "id": "ELEKTRONIK",
                        "issue_date": self.format_date(invoice.invoice_date),
                        "document_type_code": "SEND_TYPE",
                    }
                )
            if provider_name == "izibiz":
                res.append(
                    {
                        "id": "1",
                        "issue_date": self.format_date(invoice.invoice_date),
                        "document_type_code": "SendingType",
                        "document_type": "KAGIT",
                    },
                )

        return res

    def get_despatch_document_reference_vals(self, invoice):
        vals = []
        if "picking_ids" in invoice._fields:
            for picking_id in invoice.picking_ids:
                if "gib_seq" in picking_id._fields:
                    vals.append(
                        {
                            "id": picking_id.gib_seq or picking_id.name,
                            "issue_date": self.format_date(picking_id.gib_create_date),
                        }
                    )
        return vals

    def _get_delivery_vals_list(self, invoice):
        if "partner_shipping_id" in invoice._fields and invoice.partner_shipping_id:
            return [
                {
                    "actual_delivery_date": False,
                    "delivery_location_vals": {
                        "delivery_address_vals": self._get_partner_address_vals(
                            invoice.partner_shipping_id
                        ),
                    },
                }
            ]
        else:
            return []

    def _get_financial_institution_vals(self, bank):
        return {
            "name": bank.name,
        }

    def _get_financial_institution_branch_vals(self, bank):
        return {
            "name": bank.name,
            "financial_institution_vals": self._get_financial_institution_vals(bank),
        }

    def _get_financial_account_vals(self, partner_bank):
        vals = {
            "id": partner_bank.acc_number.replace(" ", ""),
        }
        if partner_bank.bank_id:
            vals["financial_institution_branch_vals"] = (
                self._get_financial_institution_branch_vals(partner_bank.bank_id)
            )

        return vals

    def _get_invoice_payment_means_vals_list(self, invoice):
        vals = {
            "payment_means_code": 30,
            "payment_due_date": self.format_date(
                invoice.invoice_date_due or invoice.invoice_date
            ),
            "instruction_note": invoice.payment_reference,
        }

        if invoice.partner_bank_id:
            vals["payee_financial_account_vals"] = self._get_financial_account_vals(
                invoice.partner_bank_id
            )

        return [vals]

    def _get_invoice_payment_terms_vals_list(self, invoice):
        payment_term = invoice.invoice_payment_term_id
        if payment_term:
            return [{"note_vals": [payment_term.name]}]
        else:
            return []

    def _get_pricing_exchange_rate_vals(self, invoice):
        if self.env.ref("base.TRY") == invoice.currency_id:
            return {}
        else:
            lines = invoice.line_ids.filtered(lambda x: x.amount_currency > 0)
            amount_currency_positive = sum(lines.mapped("amount_currency"))
            total_debit = sum(invoice.line_ids.mapped("debit"))
            if "custom_currency_rate" in invoice._fields:
                currency_rate_amount = invoice.custom_currency_rate
            else:
                currency_rate_amount = float_repr(total_debit / amount_currency_positive, 6)
            return {
                "source_currency_code": invoice.currency_id.name,
                "target_currency_code": invoice.company_id.currency_id.name,
                "calculation_rate": currency_rate_amount,
                "pricing_exchange_rate_vals": False,
            }

    def _get_invoice_tax_category_vals(self, vals):
        return {
            "name": False,
            "tax_scheme_name": vals.get("tax_group_name"),
            "tax_scheme_tax_type_code": vals.get("tax_group"),
        }

    def _get_invoice_tax_totals_vals_list(self, invoice, taxes_vals):
        return [
            {
                "currency_name": invoice.currency_id.name,
                "currency_dp": invoice.currency_id.decimal_places,
                "tax_amount": abs(taxes_vals["tax_amount_currency"]),
                "tax_subtotal_vals": [
                    {
                        "currency_name": invoice.currency_id.name,
                        "currency_dp": invoice.currency_id.decimal_places,
                        "taxable_amount": abs(vals["base_amount_currency"]),
                        "tax_amount": abs(vals["tax_amount_currency"]),
                        "percent": int(vals["amount"]),
                        "tax_category_vals": self._get_invoice_tax_category_vals(vals),
                    }
                    for vals in taxes_vals["tax_details"].values()
                ],
            }
        ]

    def _get_invoice_line_item_vals(self, line):
        product = line.product_id
        description = line.name and line.name.replace("\n", ", ")

        return {
            "name": description,
            "sellers_item_identification_vals": {"id": product.code},
        }

    def _get_document_allowance_charge_vals_list(self, invoice):
        invoice_lines = invoice.invoice_line_ids.filtered(
            lambda line: line.display_type not in ("line_note", "line_section")
        )
        vals_list = []
        for line in invoice_lines:
            res = self._get_invoice_line_allowance_vals_list(line)
            vals_list += res
        return vals_list

    def _get_invoice_line_allowance_vals_list(self, line):
        if not line.discount:
            return []

        net_price_subtotal = line.price_subtotal
        if line.discount == 100.0:
            gross_price_subtotal = 0.0
        else:
            gross_price_subtotal = line.currency_id.round(
                net_price_subtotal / (1.0 - (line.discount or 0.0) / 100.0)
            )

        allowance_vals = {
            "currency_name": line.currency_id.name,
            "currency_dp": line.currency_id.decimal_places,
            "charge_indicator": "false",
            "amount": gross_price_subtotal - net_price_subtotal,
        }

        return [allowance_vals]

    def _get_invoice_line_price_vals(self, line):
        net_price_subtotal = line.price_subtotal
        if line.discount == 100.0:
            gross_price_subtotal = 0.0
        else:
            gross_price_subtotal = net_price_subtotal / (
                1.0 - (line.discount or 0.0) / 100.0
            )
        gross_price_unit = line.currency_id.round(
            (gross_price_subtotal / line.quantity) if line.quantity else 0.0
        )
        uom = self._get_uom_unece_code(line.product_uom_id)
        return {
            "currency_name": line.currency_id.name,
            "currency_dp": line.currency_id.decimal_places,
            "price_amount": line.price_unit,
            "base_quantity": False,
            "base_quantity_attrs": {"unitCode": uom},
        }

    def _get_line_delivery_vals(self, line):
        return {
            "delivery_terms": line.move_id.invoice_incoterm_id.code,
            "delivery_terms_attrs": {"schemeID": "INCOTERMS"},
            "shipment_vals": {
                "id": "000",
                "currency_name": line.move_id.currency_id.name,
                "currency_dp": line.move_id.currency_id.decimal_places,
                "goods_item_list": [
                    {
                        "required_customs_id": (
                            line.product_id.product_tmpl_id.hs_code
                            if "hs_code" in line.product_id.product_tmpl_id
                            else False
                        )
                    }
                ],
                "shipment_stage_vals": {
                    "transport_mode_code": (
                        line.move_id.gib_delivery_type
                        if "gib_delivery_type" in line.move_id
                        else False
                    ),
                },
            },
        }

    def _get_invoice_line_vals(self, line, taxes_vals):
        allowance_charge_vals_list = self._get_invoice_line_allowance_vals_list(line)

        uom = self._get_uom_unece_code(line.product_uom_id)

        return {
            "id": line.id,
            "currency_name": line.currency_id.name,
            "currency_dp": line.currency_id.decimal_places,
            "invoiced_quantity": line.quantity,
            "invoiced_quantity_attrs": {"unitCode": uom},
            "line_extension_amount": line.price_subtotal,
            "delivery_vals": self._get_line_delivery_vals(line),
            "allowance_charge_vals": allowance_charge_vals_list,
            "tax_total_vals": self._get_invoice_tax_totals_vals_list(
                line.move_id, taxes_vals
            ),
            "item_vals": self._get_invoice_line_item_vals(line),
            "price_vals": self._get_invoice_line_price_vals(line),
        }

    def _export_invoice_vals(self, invoice):

        def grouping_key_generator(base_line, tax_values):
            tax = tax_values["tax_repartition_line"].tax_id

            grouping_key = {
                "tax_group": tax.tax_group_id.code,
                "tax_group_name": tax.tax_group_id.name,
                "amount": tax.amount,
            }
            return grouping_key

        self._validate_taxes(invoice)
        taxes_vals = invoice._prepare_edi_tax_details(
            grouping_key_generator=grouping_key_generator
        )

        line_extension_amount = 0.0

        invoice_lines = invoice.invoice_line_ids.filtered(
            lambda line: line.display_type not in ("line_note", "line_section")
        )
        document_allowance_charge_vals_list = (
            self._get_document_allowance_charge_vals_list(invoice)
        )
        invoice_line_vals_list = []
        for idx, line in enumerate(invoice_lines, 1):
            line_taxes_vals = taxes_vals["tax_details_per_record"][line]
            line_vals = self._get_invoice_line_vals(line, line_taxes_vals)
            line_vals.update({"id": idx})
            invoice_line_vals_list.append(line_vals)
            line_extension_amount += line_vals["line_extension_amount"]

        allowance_total_amount = 0.0
        for allowance_charge_vals in document_allowance_charge_vals_list:
            if allowance_charge_vals["charge_indicator"] == "false":
                allowance_total_amount += allowance_charge_vals["amount"]

        supplier = invoice.company_id.partner_id.commercial_partner_id
        customer = (
            invoice.partner_id
            if invoice.partner_id.type == "invoice"
            else invoice.commercial_partner_id
        )
        order_reference_vals = {}
        sales_order_id = (
            "sale_line_ids" in invoice.invoice_line_ids._fields
            and ",".join(invoice.invoice_line_ids.sale_line_ids.order_id.mapped("name"))
        )
        if sales_order_id:
            first_sales_order_id = invoice.invoice_line_ids.sale_line_ids.order_id[:1]
            order_reference_vals = {
                "id": sales_order_id,
                "issue_date": self.format_date(first_sales_order_id.date_order),
            }

        # Note bolümü
        notes = [html2plaintext(invoice.narration)] if invoice.narration else []

        # TODO hazır notlara çekilecek
        display_lots = None
        # display_lots = self.env.ref('stock_account.group_lot_on_invoice')
        lot_values = display_lots and invoice._get_invoiced_lot_values() or []
        for snln_line in lot_values:
            notes.append(
                f"""SN/LN:{snln_line['quantity']} {snln_line['uom_name']} {snln_line['product_name']}: {snln_line['lot_name']}"""
            )
        if invoice.ref:
            notes.append(f"""Müşteri Referansı:{invoice.ref}""")

        result = {
            "vals": {
                "ubl_version_id": 2.1,
                "customization_id": "TR1.2",
                "profile_id": invoice.gib_profile_id.value,
                "id": invoice.gib_invoice_name,
                "copy_indicator": "false",
                "uuid": invoice.gib_uuid,
                "issue_date": self.format_date(invoice.invoice_date),
                "issue_time": self.format_time(),
                "due_date": self.format_date(invoice.invoice_date_due),
                "note_vals": notes,
                "invoice_type_code": invoice.gib_invoice_type_id.value,
                "line_count_numeric": len(invoice_lines),
                "order_reference": order_reference_vals,
                "sales_order_id": sales_order_id,
                "despatch_document_reference_vals_list": self.get_despatch_document_reference_vals(
                    invoice
                ),
                "additional_document_reference_vals_list": self._get_additional_document_reference_vals(
                    invoice
                ),
                "signature_vals": {},
                "accounting_supplier_party_vals": {
                    "party_vals": self._get_partner_party_vals(
                        supplier, role="supplier"
                    ),
                },
                "accounting_customer_party_vals": {
                    "party_vals": self._get_partner_party_vals(
                        customer, role="customer"
                    ),
                },
                "delivery_vals_list": self._get_delivery_vals_list(invoice),
                "payment_means_vals_list": self._get_invoice_payment_means_vals_list(
                    invoice
                ),
                "payment_terms_vals": self._get_invoice_payment_terms_vals_list(
                    invoice
                ),
                "pricing_exchange_rate_vals": self._get_pricing_exchange_rate_vals(
                    invoice
                ),
                "tax_total_vals": self._get_invoice_tax_totals_vals_list(
                    invoice, taxes_vals
                ),
                "legal_monetary_total_vals": {
                    "currency_name": invoice.currency_id.name,
                    "currency_dp": invoice.currency_id.decimal_places,
                    "line_extension_amount": line_extension_amount,
                    "tax_exclusive_amount": invoice.amount_untaxed,
                    "tax_inclusive_amount": invoice.amount_total,
                    "allowance_total_amount": allowance_total_amount,
                    "payable_amount": invoice.amount_total,
                },
                "invoice_line_vals": invoice_line_vals_list,
                "currency_dp": invoice.currency_id.decimal_places,
                "currency_name": invoice.currency_id.name.upper(),
            },
        }
        return result

    def _export_invoice(self, invoice):
        vals = self._export_invoice_vals(invoice)
        provider = invoice._get_gib_provider()
        return self.get_authenticate_on_server(provider, "invoice", vals)

    def _get_url(self, app="invoice"):
        if app != "invoice":
            return super()._get_url(app)
        return self._get_base_url("ubl/v1/invoice")
