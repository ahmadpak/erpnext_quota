import frappe
import json
import os
import subprocess
from frappe.utils import cint
from frappe import _

def user_limit(self, cdt):
  with open(frappe.get_site_path('quota.json')) as jsonfile:
      parsed = json.load(jsonfile)
  allowed_users = parsed["users"]
  user_list = frappe.get_list('User', filters = {
    'enabled': 1,
    'name': ['!=','Guest']
  }, page_length = 2000000)
  if len(user_list)>= allowed_users:
    if not frappe.get_list('User', filters={
      'name': self.name
    }):
      frappe.throw('Only {} active users allowed and you have {} active users. Please disable users or to increase the limit please contact sales'. format(allowed_users, len(user_list))) 
    elif self.enabled == 1 and len(user_list) > allowed_users:
      frappe.throw('Only {} active users allowed and you have {} active users. Please disable users or to increase the limit please contact sales'. format(allowed_users, len(user_list)-1)) 

  data = {}
  with open(frappe.get_site_path('quota.json')) as outfile:
    data = json.load(outfile)
  data['active_users'] = len(user_list)

  with open(frappe.get_site_path('quota.json'), 'w') as outfile:
    json.dump(data, outfile)


def space_limit(self, cdt):
  with open(frappe.get_site_path('quota.json')) as jsonfile:
      parsed = json.load(jsonfile)
  allowed_users = parsed["users"]
  allowed_space = parsed["space"]

  user_list = frappe.get_list('User', filters = {
      'enabled': 1,
      'name': ['!=','Guest']
    }, page_length = 2000000)

  if len(user_list)> allowed_users:
      frappe.throw('Only {} active users allowed and you have {} active users.Please disable users or to increase the limit please contact sales'. format(allowed_users, len(user_list))) 

  total_size = ""
  output_string = subprocess.check_output(["du","-s","--block-size=1M",frappe.get_site_path()])
  for char in output_string:
    if chr(char) == "\t":
      break
    else:
      total_size += chr(char)

  total_size = int(total_size)

  if total_size > allowed_space:
    frappe.throw('You have exceeded your space limit. Delete some files from file manager or to incease the limit please contact sales')


  data = {}
  with open(frappe.get_site_path('quota.json')) as outfile:
    data = json.load(outfile)
  data['used_space'] = total_size

  with open(frappe.get_site_path('quota.json'), 'w') as outfile:
    json.dump(data, outfile)

def company_limit(self,method):
  with open(frappe.get_site_path('quota.json')) as jsonfile:
      limit_setting = json.load(jsonfile)
  total_company = len(frappe.db.get_all('Company',filters={}))
  if total_company >= cint(limit_setting.get('company')):
    if not frappe.get_list('Company', filters={
      'name': self.name
    }):  
      frappe.throw(_("Only {} company allowed and you have {} company.Please remove other company or to increase the limit please contact sales").format(limit_setting.get('company'),total_company))
  with open(frappe.get_site_path('quota.json')) as outfile:
    data = json.load(outfile)
    data['used_company'] = total_company
  with open(frappe.get_site_path('quota.json'), 'w') as outfile:
    json.dump(data, outfile)
