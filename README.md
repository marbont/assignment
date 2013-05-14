# Assignment

## Setup
* ** Requirements installation **
  pip install -r requeriments/0-production.txt
* ** Create your own settings_local.py **
  cp settings_local_template.py settings_local.py
* ** Configure your own settings_local.py **
  Enter all needed values in settings_local.py
* ** Fixtures loading **  
  python manage.py loaddata
  You can use the account admin (password: admin) to manage admin site
  
## Usage
* Once the server is running you can insert (thorugh the admin panel) new account or delete old ones: they will be automatically synchronized with remote DB.
The admin panel will be available on the following url: http://127.0.0.1:8000/admin
* The local DB can be synchronized using this command: python assignment/account_lead/cron/update_local_db.py
You can configure your crontab to schedule it.
* The API endpoint to manage account lead entities is: http://127.0.0.1:8000/api/v1/account_lead/
You have to append this GET params: {username=tb, api_key=e37dbf8facc2d9fe96b8a2c75fab91431b10b05e, format=json}
* A search function is available at http://127.0.0.1:8000/search/
* Tests can be launched through this command:
python manage.py test account_lead
