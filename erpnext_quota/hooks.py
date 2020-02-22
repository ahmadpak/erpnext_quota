# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "erpnext_quota"
app_title = "Erpnext Quota"
app_publisher = "Havenir Solutions Private Limited"
app_description = "App to manage ERPNext User and Space limitations"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@havenir.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_quota/css/erpnext_quota.css"
# app_include_js = "/assets/erpnext_quota/js/erpnext_quota.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_quota/css/erpnext_quota.css"
# web_include_js = "/assets/erpnext_quota/js/erpnext_quota.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "erpnext_quota.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

before_install = "erpnext_quota.install.before_install"
# after_install = "erpnext_quota.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_quota.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doc_events = {
  'User': {
    'validate': 'erpnext_quota.erpnext_quota.quota.user_limit',
    'on_update': 'erpnext_quota.erpnext_quota.quota.user_limit'
  },
  '*': {
    'submit': 'erpnext_quota.erpnext_quota.quota.space_limit'
  },
  'File': {
    'validate': 'erpnext_quota.erpnext_quota.quota.space_limit'
  }
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"erpnext_quota.tasks.all"
# 	],
# 	"daily": [
# 		"erpnext_quota.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnext_quota.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnext_quota.tasks.weekly"
# 	]
# 	"monthly": [
# 		"erpnext_quota.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "erpnext_quota.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpnext_quota.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "erpnext_quota.task.get_dashboard_data"
# }

