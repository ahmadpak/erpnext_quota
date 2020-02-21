import frappe
import json
import os
import subprocess

def user_limit(self, cdt):
  with open(frappe.get_site_path('quota.json')) as jsonfile:
      parsed = json.load(jsonfile)
  allowed_users = parsed["users"]
  user_list = frappe.get_list('User', filters = {
    'enabled': 1
  }, page_length = 2000000)

  if len(user_list)>= allowed_users:
    if not frappe.get_list('User', filters={
      'name': self.name
    }):
      frappe.throw('Only {} active users allowed. To increase the limit please contact sales'. format(allowed_users)) 
  
  else:
    usage_doc = frappe.get_doc('Usage Info')
    usage_doc.db_set('users_allowed', allowed_users)
    usage_doc.db_set('active_users', len(user_list))


def space_limit(self, cdt):
  with open(frappe.get_site_path('quota.json')) as jsonfile:
      parsed = json.load(jsonfile)
  allowed_space = parsed["space"]
  total_size = ""
  # total_size = subprocess.check_output(['du','-sh',frappe.get_site_path]).split()[0].decode('utf-8')
  output_string = subprocess.check_output(["du","-s","--block-size=1M",frappe.get_site_path()])
  for char in output_string:
    if chr(char) == "\t":
      break
    else:
      total_size += chr(char)

  total_size = int(total_size)

  if total_size > allowed_space:
    frappe.throw('You have exceeded your space limit. To incease the limit please contact sales')
  else:
    usage_doc = frappe.get_doc('Usage Info')
    usage_doc.db_set('space_allowed', allowed_space)
    usage_doc.db_set('used_space', total_size)

  data = {}
  with open(frappe.get_site_path('quota.json')) as outfile:
    data = json.load(outfile)
  data['used_space'] = total_size

  with open(frappe.get_site_path('quota.json'), 'w') as outfile:
    json.dump(data, outfile)