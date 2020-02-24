import frappe
import json
import os

def before_install():
  data = {}
  data['users'] = 5
  data['space'] = 5120
  data['company'] = 2
  with open(frappe.get_site_path('quota.json'), 'w') as outfile:
    json.dump(data, outfile)
    
  # if outfile:
  print('file quota.json created at', frappe.get_site_path('quota.json'))
  print('Change the value of users,space and company in quota.json to change limits')