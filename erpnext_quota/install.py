import frappe
from frappe.installer import update_site_config
from frappe.utils.data import add_days, today


def before_install():
    filters = {
        'enabled': 1,
        'name': ['not in', ['Guest', 'Administrator']]
    }

    user_list = frappe.get_all('User', filters=filters, fields=["name"])

    active_users = 0

    for user in user_list:
        roles = frappe.get_all(
            "Has Role",
            filters={
                'parent': user.name
            },
            fields=['role']
        )

        for row in roles:
            if frappe.get_value("Role", row.role, "desk_access") == 1:
                active_users += 1
                break

    data = {
        'users': 5,
        'active_users': active_users,
        'space': 0,
        'db_space': 0,
        'company': 2,
        'used_company': 1,
        'count_website_users': 0,
        'count_administrator_user': 0,
        'valid_till': add_days(today(), 14),
        'document_limit': {
            'Sales Invoice': {'limit': 10, 'period': 'Daily'},
            'Purchase Invoice': {'limit': 10, 'period': 'Weekly'},
            'Journal Entry': {'limit': 10, 'period': 'Monthly'},
            'Payment Entry': {'limit': 10, 'period': 'Monthly'}
        }
    }

    # Updating site config
    update_site_config('quota', data)
