# -*- coding: utf-8 -*-
# Copyright (c) 2020, Havenir Solutions Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document


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
        for item in document_limit:
            self.append('document_limit', item)
        self.save()
        self.reload()
