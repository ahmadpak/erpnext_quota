from __future__ import unicode_literals
from frappe import _
from frappe.desk.moduleview import add_setup_section

def get_data():
    data = [
        {
            "label": _("Settings"),
            "icon": "fa fa-wrench",
            "items": [
                {
                    "type": "doctype",
                    "name": "Usage Info",
                    "label": _("Usage Info"),
                    "hide_count": True,
                    "settings": 1,
                }
            ]
        }
    ]

    return data