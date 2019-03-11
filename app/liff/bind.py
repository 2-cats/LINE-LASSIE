'''
LINE account with Goodlinker AWS user

Created at 2018/12/26 by Eric
'''
import json
import requests
from flask import Flask
from linebot.models import ButtonsTemplate, TemplateSendMessage, URIAction

from .. import db
from ..models import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')


# Try bind user between LINE and AWS Cognito
def bind_user(email, phone, line_user_id):
    phone = phone.replace('0', '+886', 1)
    check_result = query_user_data(email, phone, line_user_id)
    return check_result

# Query user data in Cognito
def query_user_data(email, phone, line_user_id):
    messages = []
    if check_line_user_id_exist(line_user_id):
        messages.append('LINE 帳號已經被綁定過')
        return messages

    # Query sensor.live end users list
    end_users_list = requests.get(
        ''.join(
            [
                app.config['SENSOR_LIVE_API_URL'],
                'projects/',
                app.config['SENSOR_LIVE_PROJECT_ID'],
                '/end_users/list'
            ]
        ),
        headers={
            'Account': app.config['SENSOR_LIVE_ACCOUNT'],
            'Authorization': app.config['SENSOR_LIVE_TOKEN']
        }
    )
    end_users_list = json.loads(end_users_list.text)
    for end_user in end_users_list['data']:
        if 'phone' in end_user:
            if end_user['phone'] == phone:
                for user_attribute in end_user['user_attributes']:
                    if user_attribute['name'] == 'custom:additional_info':
                        if user_attribute['value'] == email:
                            if check_username_exist(end_user['username']):
                                return messages.append('帳號已經被綁定過')
                            else:
                                bind_line_user_id(end_user['username'], line_user_id)
                                return 0
        elif 'email' in end_user:
            if end_user['email'] == email:
                for user_attribute in end_user['user_attributes']:
                    if user_attribute['name'] == 'custom:additional_info':
                        if user_attribute['value'] == phone:
                            if check_username_exist(end_user['username']):
                                return messages.append('帳號已經被綁定過')
                            else:
                                bind_line_user_id(end_user['username'], line_user_id)
                                return 0
    messages.append('找不到使用者')
    return messages

# Check aws_username is exist
def check_username_exist(username):
    user = User.query.filter_by(
        aws_user_name=username,
        deleted_at=None
    ).first()
    if user is None:
        return False
    return True

def check_line_user_id_exist(line_user_id):
    user = User.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()
    if user is None:
        return False
    return True

# Bind user to RDS table: USERS
def bind_line_user_id(username, line_user_id):
    user = User(
        line_user_id=line_user_id,
        aws_user_name=username
    )

    db.session.add(user)
    try:
        db.session.commit()
        User.link_rm_to_user(user)
    except:
        pass
