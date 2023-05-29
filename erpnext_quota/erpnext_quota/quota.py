import subprocess

import frappe
from frappe import _
from frappe.installer import update_site_config
from frappe.utils import get_first_day, get_first_day_of_week, getdate


# User
def user_limit(self, method):
    quota = frappe.get_site_config()['quota']
    count_website_users = quota["count_website_users"]
    count_administrator_user = quota["count_administrator_user"]
    allowed_users = quota["users"]
    active_users = validate_users(self, count_administrator_user, count_website_users, allowed_users)
    quota['active_users'] = active_users

    # updating site config
    update_site_config('quota', quota)


def validate_users(self, count_administrator_user, count_website_users, allowed_users):
    '''
    Validates and returns active users
    Params:
    1. self
    2. count_administrator_user => (bool) => either count administrator or not
    3. count_website_users => (bool) => either count website users or not
    4. allowed_users => (int) => maximum users allowed
    '''
    # allowed user value type check
    if type(allowed_users) is not int:
        frappe.throw(_("Invalid value for maximum User Allowed limit. it can be a whole number only."), frappe.ValidationError)

    # Fetching all active users list
    filters = {
        'enabled': 1,
        "name": ['!=', 'Guest']
    }

    # if we don't have to count administrator also
    if count_administrator_user == 0:
        filters['name'] = ['not in', ['Guest', 'Administrator']]

    user_list = frappe.get_all('User', filters, ["name"])
    active_users = len(user_list)
    is_desk = ""

    # if don't have to count website users
    if not count_website_users:
        active_users = 0
        is_desk = "Desk"

    for user in user_list:
        roles = frappe.get_all("Has Role", {'parent': user.name}, ['role'])
        for row in roles:
            if frappe.get_value("Role", row.role, "desk_access") == 1:
                active_users += 1
                break

    # Users limit validation
    if allowed_users != 0 and active_users >= allowed_users:
        if not frappe.get_all('User', filters={'name': self.name}):
            frappe.throw('Only {} active {} users allowed and you have {} active users. Please disable users or to increase the limit please contact sales'. format(allowed_users, is_desk, active_users))

    return active_users


# Files
def files_space_limit(self, method):
    validate_files_space_limit()


def validate_files_space_limit():
    '''
    Validates files space limit
    '''

    # Site config
    quota = frappe.get_site_config()['quota']

    allowed_space = quota["space"]

    # allowed space value type check
    if type(allowed_space) is not int:
        frappe.throw(_("Invalid value for maximum Space limit. It can be a whole number only."), frappe.ValidationError)

    # all possible file locations
    site_path = frappe.get_site_path()
    private_files_path = site_path + '/private/files'
    public_files_path = site_path + '/public/files'
    backup_files_path = site_path + '/private/backups'

    # Calculating Sizes
    total_size = get_directory_size(site_path)
    private_files_size = get_directory_size(private_files_path)
    public_files_size = get_directory_size(public_files_path)
    backup_files_size = get_directory_size(backup_files_path)

    # Writing File
    quota['used_space'] = total_size
    quota['private_files_size'] = private_files_size
    quota['public_files_size'] = public_files_size
    quota['backup_files_size'] = backup_files_size

    update_site_config('quota', quota)

    if allowed_space != 0 and total_size > allowed_space:
        msg = '''
        <div>You have exceeded your files space limit. Delete some files from file manager or to increase the limit please contact sales</div>
        <div><ul><li>Private Files: {}MB</li><li>Public Files: {}MB</li><li>Backup Files: {}MB</li></ul></div>
        '''.format(private_files_size, public_files_size, backup_files_size)

        frappe.throw(_(msg))


# DB
def db_space_limit(self, method):
    validate_db_space_limit()


def validate_db_space_limit():
    '''
    Validates DB space limit
    '''
    # Site config
    quota = frappe.get_site_config()['quota']
    allowed_db_space = quota["db_space"]

    # allowed DB space value type check
    if type(allowed_db_space) is not int:
        frappe.throw(_("Invalid value for maximum Database Space limit. it can be a whole number only."), frappe.ValidationError)

    # Getting DB Space
    used_db_space = frappe.db.sql('''SELECT `table_schema` as `database_name`, SUM(`data_length` + `index_length`) / 1024 / 1024 AS `database_size` FROM information_schema.tables  GROUP BY `table_schema`''')[1][1]
    used_db_space = int(used_db_space)

    # Updating quota config
    quota['used_db_space'] = used_db_space

    update_site_config('quota', quota)

    if allowed_db_space != 0 and used_db_space > allowed_db_space:
        msg = '''
        <div>You have exceeded your Database Size limit. Please contact sales to upgrade your package</div>
        <ul><li>Allowed Space: {}MB</li><li>Used Space: {}MB</li></ul>
        '''.format(allowed_db_space, used_db_space)
        frappe.throw(_(msg))


# Company
def company_limit(self, method):
    '''
    Validates Company limit
    '''

    quota = frappe.get_site_config()['quota']
    allowed_companies = quota.get('company')

    # allowed Companies value type check
    if type(allowed_companies) is not int:
        frappe.throw(_("Invalid value for maximum allowed Companies limit. it can be a whole number only."), frappe.ValidationError)

    # Calculating total companies
    total_company = len(frappe.db.get_all('Company', filters={}))
    quota['used_company'] = total_company

    # Updating site config
    update_site_config('quota', quota)

    # Validation
    if allowed_companies != 0 and total_company >= allowed_companies:
        if not frappe.get_all('Company', {'name': self.name}):
            frappe.throw(_("Only {} company(s) allowed and you have {} company(s).Please remove other company or to increase the limit please contact sales").format(quota.get('company'), total_company))


# Directory Size
def get_directory_size(path):
    '''
    returns total size of directory in MBss
    '''
    output_string = subprocess.check_output(["du", "-mcs", "{}".format(path)])
    total_size = ''
    for char in output_string:
        if chr(char) == "\t":
            break
        else:
            total_size += chr(char)

    return int(total_size)


def document_limit(doc, event):
    """
    We check for the doctype in document_limit and compute accordingly.
    """
    limit_dict = frappe.get_site_config()['quota']['document_limit']
    if (limit_dict.get(doc.doctype)):
        limit = frappe._dict(limit_dict.get(doc.doctype))
        limit_period = get_limit_period(limit.period)
        usage = len(frappe.db.get_all(
            doc.doctype,
            filters={
                'creation': ['BETWEEN', [str(limit_period.start) + ' 00:00:00.000000', str(limit_period.end) + ' 23:59:59.999999']]
            }))
        if usage >= limit.limit:
            msg = _(f"Your have reached your {doc.doctype} {limit.period} limit of {limit.limit} and hench cannot create new document. Please contact administrator.")
            frappe.throw(msg, title="Quota Limit")


def get_limit_period(period):
    """
        Get date mappinf for document limit period
    """
    today = getdate()
    week_start = get_first_day_of_week(today)
    periods = {
        'Daily': {'start': str(today), 'end': str(today)},
        'Weekly': {'start': str(week_start), 'end': str(today)},
        'Monthly': {'start': str(get_first_day(today)), 'end': str(today)},
    }
    return frappe._dict(periods.get(period))
