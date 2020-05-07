import os

#All variables are loaded from heroku config variables


#Twilio config----------------------------------------

#Twilio account_sid
tw_account_sid = os.environ.get("tw_account_sid")

#Twilio auth token
tw_auth_token = os.environ.get("tw_auth_token")

#Url for twilio xml
tw_xml = os.environ.get("tw_xml")

#From number in twilio
tw_from_number = os.environ.get("tw_from_number")

#Discord config---------------------------------------------

#Discord bot token
dc_token = os.environ.get("dc_token")

#Discord admin user id
dc_admin_id = int(os.environ.get("dc_admin_id"))

#Discord id of the channel where @everyone will call
dc_channel_id = int(os.environ.get("dc_channel_id"))

#Database config-------------------------------------------------

#Database host
db_host = os.environ.get("db_host")
#Database user
db_user = os.environ.get("db_user")
#Database password
db_pass = os.environ.get("db_pass")
#Database name
db_name = os.environ.get("db_name")

#Fernet config---------------------------------------------

#Fernet key !!DONT CHANGE THIS OR NUMBERS WILL BE LOST
f_secret_key = os.environ.get("f_secret_key").encode()

#Misc config-----------------------------------------------
#Debug mode 1 for true 0 for false (listnumbers etc.)
debug = int(os.environ.get("debug"))