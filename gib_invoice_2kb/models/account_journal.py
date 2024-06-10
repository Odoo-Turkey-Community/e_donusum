# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import datetime
from odoo import models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def _compute_to_entries_count(self):
        res = [
            (r["journal_id"][0], r["journal_id_count"], r["amount_total"])
            for r in self.env["account.move"]._read_group(
                domain=[
                    ("journal_id", "in", self.ids),
                    ("gib_state", "in", ["to_send", "to_cancel"]),
                ],
                fields=["journal_id", "amount_total"],
                groupby=["journal_id"],
            )
        ]
        return res

    def _compute_rejected_and_waiting_count(self):
        res = [
            (r["journal_id"][0], r["journal_id_count"], r["amount_total"])
            for r in self.env["account.move"]._read_group(
                domain=[
                    ("journal_id", "in", self.ids),
                    ("gib_response_code", "=", "reject"),
                    ("state", "not in", ["cancel"]),
                ],
                fields=["journal_id", "amount_total"],
                groupby=["journal_id"],
            )
        ]
        return res

    def _compute_undelivered_count(self):
        res = [
            (r["journal_id"][0], r["journal_id_count"], r["amount_total"])
            for r in self.env["account.move"]._read_group(
                domain=[
                    ("journal_id", "in", self.ids),
                    (
                        "gib_status_code_id_value2",
                        "in",
                        ["error"],
                    ),
                    ("state", "not in", ["cancel"]),
                ],
                fields=["journal_id", "amount_total"],
                groupby=["journal_id"],
            )
        ]
        return res

    def _compute_external_cancellation(self):
        res = [
            (r["journal_id"][0], r["journal_id_count"], r["amount_total"])
            for r in self.env["account.move"]._read_group(
                domain=[
                    (
                        "invoice_date",
                        ">",
                        datetime.datetime.today() - datetime.timedelta(days=60),
                    ),
                    ("journal_id", "in", self.ids),
                    ("external_cancellation", "!=", False),
                    ("state", "in", ["cancel"]),
                ],
                fields=["journal_id", "amount_total"],
                groupby=["journal_id"],
            )
        ]
        return res

    def _fill_sale_purchase_dashboard_data(self, dashboard_data):
        super(AccountJournal, self)._fill_sale_purchase_dashboard_data(dashboard_data)
        sale_purchase_journals = self.filtered(
            lambda journal: journal.type in ("sale", "purchase")
        )
        if not sale_purchase_journals:
            return
        sale_purchase_journals_vals = sale_purchase_journals._compute_to_entries_count()
        for journal_id in sale_purchase_journals:
            vals = filter(
                lambda item: item[0] == journal_id.id, sale_purchase_journals_vals
            )
            for val in vals:
                currency_id = journal_id.currency_id or self.company_id.currency_id
                if sale_purchase_journals_vals:
                    dashboard_data[journal_id.id].update(
                        {
                            "gib_to_process": val[1],
                            "amount": currency_id.format(val[2]),
                        }
                    )

        rejected_and_waiting_count = (
            sale_purchase_journals._compute_rejected_and_waiting_count()
        )
        for journal_id in sale_purchase_journals:
            vals = filter(
                lambda item: item[0] == journal_id.id, rejected_and_waiting_count
            )
            for val in vals:
                currency_id = journal_id.currency_id or self.company_id.currency_id
                if rejected_and_waiting_count:
                    dashboard_data[journal_id.id].update(
                        {
                            "rejected_and_waiting_to_action": val[1],
                            "amount_rejected_and_waiting": currency_id.format(val[2]),
                        }
                    )

        undelivered_count = sale_purchase_journals._compute_undelivered_count()
        for journal_id in sale_purchase_journals:
            vals = filter(lambda item: item[0] == journal_id.id, undelivered_count)
            for val in vals:
                currency_id = journal_id.currency_id or self.company_id.currency_id
                if undelivered_count:
                    dashboard_data[journal_id.id].update(
                        {
                            "undelivered_count": val[1],
                            "amount_undelivered_count": currency_id.format(val[2]),
                        }
                    )

        external_cancellation = sale_purchase_journals._compute_external_cancellation()
        for journal_id in sale_purchase_journals:
            vals = filter(lambda item: item[0] == journal_id.id, external_cancellation)
            for val in vals:
                currency_id = journal_id.currency_id or self.company_id.currency_id
                if external_cancellation:
                    dashboard_data[journal_id.id].update(
                        {
                            "external_cancellation": val[1],
                            "amount_external_cancellation": currency_id.format(val[2]),
                        }
                    )

    def open_action(self):
        res = super().open_action()
        to_redirect = self.env.context.get("action_to")
        if to_redirect not in [
            "to_rejected_and_waiting",
            "to_undelivered_count",
            "to_external_cancellation",
        ]:
            return res

        if to_redirect == "to_rejected_and_waiting":
            res["views"][0] = (
                self.env.ref(
                    "gib_invoice_2kb.view_out_invoice_rejected_and_waiting"
                ).id,
                "tree",
            )

        if to_redirect == "to_undelivered_count":
            res["views"][0] = (
                self.env.ref("gib_invoice_2kb.view_out_invoice_undelivered_count").id,
                "tree",
            )
        if to_redirect == "to_external_cancellation":
            res["views"][0] = (
                self.env.ref(
                    "gib_invoice_2kb.view_out_invoice_external_cancellation"
                ).id,
                "tree",
            )
        return res

    def _get_move_action_context(self):
        ctx = super()._get_move_action_context()
        return ctx
