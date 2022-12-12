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

        for key, value in usage.items():
            self.db_set(key, value)
