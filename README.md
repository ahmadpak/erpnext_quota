## Erpnext Quota

App to manage ERPNext User, Company and Space limitations

#### How to Install
```
bench get-app https://github.com/ahmadpak/erpnext_quota
bench --site *site_name* install-app erpnext_quota
```
### Usage
Install the app. It will add quota config in the site_config.json file
Contents will look similar:

```json
{
 "db_name": "_153e0b60307d7518",
 "db_password": "LrhxSwya9SlAfjAa",
 "db_type": "mariadb",
 "encryption_key": "IcfnBCemM-aDs6Xe9RErXLMlXsDdM1nfC4q3jg7_PFE=",
 "quota": {
  "active_users": 6,
  "backup_files_size": 29,
  "company": 2,
  "count_administrator_user": 0,
  "count_website_users": 0,
  "db_space": 0,
  "document_limit": {
    "Sales Invoice": {"limit": 10, "period": "Daily"},
    "Purchase Invoice": {"limit": 10, "period": "Weekly"},
    "Journal Entry": {"limit": 10, "period": "Monthly"},
    "Payment Entry": {"limit": 10, "period": "Monthly"}
  },
  "private_files_size": 0,
  "public_files_size": 3,
  "space": 0,
  "used_company": 1,
  "used_space": 31,
  "users": 5,
  "valid_till": "2023-03-19"
 },
 "user_type_doctype_limit": {
  "employee_self_service": 20
}
```

Manually change the default values to change the limits. 
Default is:
- 5 active users not including website users
- 2 companies

quota.json file will automatically get updated for any 

To view the Usage info, find it in Settings Module or search 'Usage Info' in the awesome bar
![Database Limit Screenshot](images/database_limit.png)
![Files Limit Screenshot](images/files_space_limit.png)
![User Limit Screenshot](images/user_limit.png)
![Login Limit Screenshot](images/login_validity.gif)
![Usage Info Screenshot](images/usage_info_doc.png)

#### License
MIT
