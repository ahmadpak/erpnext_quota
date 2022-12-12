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
 "db_name": "_93245f986574151a",
 "db_password": "NQaBCOxtDUDWNJiP",
 "db_type": "mariadb",
 "quota": {
  "active_users": 2,
  "backup_files_size": 2,
  "company": 2,
  "count_administrator_user": 0,
  "count_website_users": 0,
  "db_space": 100,
  "private_files_size": 0,
  "public_files_size": 0,
  "space": 5120,
  "used_company": 1,
  "used_db_space": 47,
  "used_space": 2,
  "users": 5,
  "valid_till": "2022-12-25"
 }
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
