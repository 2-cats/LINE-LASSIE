'''
LINE account with Goodlinker AWS user

Created at 2018/12/26 by Eric
'''
import datetime

import requests
from flask import Flask
from linebot.models import ButtonsTemplate, TemplateSendMessage, URIAction

import config

from .. import db
from ..models import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')


# Try bind user between LINE and AWS Cognito
def bind_user(email, phone, line_user_id):
    phone = phone.replace('0', '+886')
    check_result = query_user_data(email, phone, line_user_id)
    return check_result

# Query user data in Cognito
def query_user_data(email, phone, line_user_id):
    if check_line_user_id_exist(line_user_id):
        return 'fail: LINE account has been bind.'
    else:
        headers = {
            'Account': app.config['SENSOR_LIVE_ACCOUNT'],
            'Authorization': app.config['SENSOR_LIVE_TOKEN']
        }
        data = requests.get(''.join(['https://api.sensor.live/api/projects/', app.config['SENSOR_LIVE_PROJECT_ID'] ,'/end_users/list']), headers=headers)
        query_data = data.json()
        for item in query_data['items']:
            if item:
                if 'phone' in item:
                    if item['phone'] == phone:
                        for user_attribute in item['user_attributes']:
                            if user_attribute['name'] == 'custom:additional_info':
                                if user_attribute['value'] == email:
                                    if check_username_exist(item['username']):
                                        return 'fail: User has been bind.'
                                    else:
                                        bind_line_user_id(item['username'], line_user_id)
                                        return 'success'
                if 'email' in item:
                    if item['email'] == email:
                        for user_attribute in item['user_attributes']:
                            if user_attribute['name'] == 'custom:additional_info':
                                if user_attribute['value'] == phone:
                                    if check_username_exist(item['username']):
                                        return 'fail: User has been bind.'
                                    else:
                                        bind_line_user_id(item['username'], line_user_id)
                                        return 'success'
        return 'fail: User not found' 

# Check aws_username is in RDS table: USERS
def check_username_exist(username):
    user = User.query.filter_by(aws_user_name=username).first()
    if user is None:
        return False
    return True

# Check line_user_id is in RDS table: USERS
def check_line_user_id_exist(line_user_id):
    user = User.query.filter_by(line_user_id=line_user_id).first()
    if user is None:
        return False
    return True
    
# Bind user to RDS table: USERS
def bind_line_user_id(username, line_user_id):
    user = User(aws_user_name=username, line_user_id=line_user_id)
    db.session.add(user)
    db.session.commit()
    User.link_rm_to_user(user)
