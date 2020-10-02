## Erpnext Quota

App to manage ERPNext User, Company and Space limitations
##### Note: Space size does not include database size.

#### How to Install
bench get-app --branch master erpnext_quota https://github.com/ahmadpak/erpnext_quota
bench include-app erpnext_quota
bench --site *site_name* install-app erpnext_quota

### Usage
Install the app. It will create a file quota.json in site directory
Contents will look like:

{
  "users": 5,
  "space": 5120,
  "company": 2,
  "count_website_users": 0,
}


Manually change the default value of users, space, company and count_website_users to change the limits. Default is 5 active users not including website users, 2 companies and 5GB space for attachments and backup

After installation and creating new users, company and submitting a document, the file quota.json will get update and look like:
{
  "users": 5,
  "space": 5120,
  "company": 2,
  "count_website_users": 0,
  "active_users": 2
}

To see the Usage info with the portal visit the page 'Usage Info'
![Usage Info Screenshot](images/usage_info.png)
![Usage Info Error Screenshot](images/usage_info_error.png)
#### License
MIT
