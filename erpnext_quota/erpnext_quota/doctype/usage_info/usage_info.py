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
    allowed_company = parsed["company"]
    count_website_users = parsed["count_website_users"]

    user_list = frappe.get_list('User', filters = {
      'enabled': 1,
      'name': ['!=','Guest']
    }, fields = ["email"])

    active_users = 0
    if count_website_users == 1 : active_users = len(user_list)
    else:
      for user in user_list:
        roles = frappe.get_list("Has Role", filters = {
          'parent': user.email
        }, fields = ['role'])
        for row in roles:
          if frappe.get_value("Role", row.role, "desk_access") == 1: 
            active_users += 1
            break


    usage_doc = frappe.get_doc('Usage Info')
    usage_doc.db_set('users_allowed', allowed_users)
    usage_doc.db_set('active_users', active_users)

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
    usage_doc.db_set('company_allowed', allowed_company)
    usage_doc.db_set('active_company',len(frappe.get_all("Company",filters={})))
    return [allowed_users, active_users, allowed_space, total_size,allowed_company,len(frappe.get_all("Company",filters={}))]
