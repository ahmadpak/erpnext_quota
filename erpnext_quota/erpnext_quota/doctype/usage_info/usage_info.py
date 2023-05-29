# -*- coding: utf-8 -*-
# Copyright (c) 2020, Havenir Solutions Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document

from erpnext_quota.erpnext_quota.quota import get_limit_period


class UsageInfo(Document):
    @frappe.whitelist()
    def get_usage_info(self):
        quota = frappe.get_site_config()['quota']
        usage = {}

        for key, value in quota.items():
            usage[key] = value

        # copy out document_limit and remove from dict
        document_limit = usage['document_limit']
        del usage['document_limit']

        for key, value in usage.items():
            self.db_set(key, value)

        # update document list table
        frappe.db.truncate("Quota Document Limit Detail")
        self.reload()
        for key, value in document_limit.items():
            period = get_limit_period(value['period'])
            value['usage'] = len(frappe.db.get_all(
                key,
                {'creation': ["BETWEEN", [f"{period.start} 00:00:00.000000", f"{period.end} 23:23:59.999999"]]}
            ))
            value['document_type'] = key
            value['from_date'] = period.start
            value['to_date'] = period.end
            self.append('document_limit', value)
        self.save()
        self.reload()
