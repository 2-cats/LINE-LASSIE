'''
LINE account with Goodlinker AWS user

Created at 2018/12/26 by Eric
'''
import datetime

import requests
from flask import Flask
from linebot.models import ButtonsTemplate, TemplateSendMessage, URIAction

import config
from rds import connect
from richmenu import link_rm_to_user

app = Flask(__name__)

# Get app config
app.config.from_object(config)

# Try bind user between LINE and AWS Cognito
def bind_user(email, phone, line_user_id):
    check_result = query_user_data(email, phone, line_user_id)
    return check_result

# Query user data in Cognito
def query_user_data(email, phone, line_user_id):
    headers = {
        'Account': app.config['SENSOR_LIVE_ACCOUNT'],
        'Authorization': app.config['SENSOR_LIVE_TOKEN']
    }
    data = requests.get(''.join(['https://api.sensor.live/api/projects/', app.config['SENSOR_LIVE_PROJECT_ID'] ,'/end_users/list']), headers=headers)
    query_data = data.json()
    for user_item in query_data["items"]:
        if (str(user_item['email']) == str(email)) and (str(user_item['phone_number']) == str(phone)):
            if not check_line_user_id_exist(user_item['username']):
                bind_line_user_id(user_item['username'], line_user_id)
                return 'success'
            return 'fail: User has been registered'
    return 'fail: User not found'

# Check aws_username is in RDS table: USERS
def check_line_user_id_exist(username):
    database = connect()
    cursor = database.cursor()
    args = (username,)
    cursor.execute("SELECT line_user_id FROM users WHERE aws_username =  %s", args)
    result = cursor.fetchone()
    database.close()
    if result:
        return True
    return False
    
# Bind user to RDS table: USERS
def bind_line_user_id(username, line_user_id):
    database = connect()
    cursor = database.cursor()
    args = (line_user_id, username, datetime.datetime.now())
    cursor.execute("INSERT INTO users(line_user_id, aws_username, created_at) VALUES (%s,%s,%s)", args)
    database.commit()
    database.close()
    link_rm_to_user(line_user_id)

# Check user is bind
def check_bind(line_user_id):
    database = connect()
    cursor = database.cursor()
    args = (line_user_id,)
    cursor.execute("SELECT aws_username FROM users WHERE line_user_id =  %s", args)
    result = cursor.fetchone()
    database.close()
    if result:
        return True
    return False
