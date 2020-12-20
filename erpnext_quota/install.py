import frappe
from frappe.utils.data import add_days, today, add_months
import json
import os

def before_install():
  # if frappe.db.get_default('desktop:home_page') != 'desktop':
  #   print('ERPNext Quota can only be install after setup wizard is completed')
  # Fetching user list
  filters = {
    'enabled': 1,
    'name': ['!=','Guest', 'Administrator']
  }
  
  user_list = frappe.get_list('User', filters = filters, fields = ["name"])

  active_users = 0
  
  for user in user_list:
    roles = frappe.get_list("Has Role", filters = {
      'parent': user.name
    }, fields = ['role'])
    for row in roles:
      if frappe.get_value("Role", row.role, "desk_access") == 1: 
        active_users += 1
        break

  data = {
    'users': 5,
    'active_users': active_users,
    'space': 5120,
    'db_space': 100,
    'company': 2,
    'used_company': 1,
    'count_website_users': 0,
    'count_administrator_user': 0,
    'valid_till': add_days(today(), 14)
  }
  with open(frappe.get_site_path('quota.json'), 'w') as outfile:
    json.dump(data, outfile, indent= 2)

  file_path = frappe.utils.get_bench_path() + '/' + \
    frappe.utils.get_site_name(frappe.local.site) + \
      '/quota.json'
  
  print('\nfile quota.json created at ', file_path, 'with the following settings:')
  for key in data: print("\t{}: {}".format(key, data[key]))
  print('\nChange the values in quota.json to change limits\n')