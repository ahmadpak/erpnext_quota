import frappe
import json
import os

def before_install():
  data = {
    'users': 5,
    'space': 5120,
    'company': 2,
    'count_website_users': 0
  }
  with open(frappe.get_site_path('quota.json'), 'w') as outfile:
    json.dump(data, outfile, indent= 2)
    
  print('file quota.json created at', frappe.get_site_path('quota.json'), 'with the following settings:')
  for key in data: print("{}: {}".format(key, data[key]))
  print('Change the value of users,space,company and count_website_users in quota.json to change limits')