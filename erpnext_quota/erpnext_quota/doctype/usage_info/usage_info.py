# -*- coding: utf-8 -*-
# Copyright (c) 2020, Havenir Solutions Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from dateutil.parser import parse
from erpnext_quota.erpnext_quota.quota import validate_users
import frappe
from frappe.model.document import Document
import json
import subprocess

class UsageInfo(Document):
  
  def get_usage_info(self):
    usage = {}
    with open(frappe.get_site_path('quota.json')) as jsonfile:
        parsed = json.load(jsonfile)

    for key, value in parsed.items():
      usage[key] = value

    for key, value in usage.items():
      self.db_set(key, value)