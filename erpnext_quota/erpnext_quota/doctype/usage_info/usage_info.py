# -*- coding: utf-8 -*-
# Copyright (c) 2020, Havenir Solutions Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
import subprocess

class UsageInfo(Document):
  def get_usage_info(self):
    with open(frappe.get_site_path('quota.json')) as jsonfile:
        parsed = json.load(jsonfile)
    allowed_users = parsed["users"]
    allowed_space = parsed["space"]

    user_list = frappe.get_list('User', filters = {
      'enabled': 1,
      'name': ['!=','Guest']
    }, page_length = 2000000)

    usage_doc = frappe.get_doc('Usage Info')
    usage_doc.db_set('users_allowed', allowed_users)
    usage_doc.db_set('active_users', len(user_list))

    total_size = ""
    output_string = subprocess.check_output(["du","-s","--block-size=1M",frappe.get_site_path()])
    for char in output_string:
      if chr(char) == "\t":
        break
      else:
        total_size += chr(char)

    total_size = int(total_size)
    usage_doc.db_set('space_allowed', allowed_space)
    usage_doc.db_set('used_space', total_size)
    return [allowed_users, len(user_list), allowed_space, total_size]
