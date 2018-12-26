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

app = Flask(__name__)

# Get app config
app.config.from_object(config)

def bind_line_message(line_user_id):
    buttons_template = ButtonsTemplate(
        title='綁定服務',
        text='您好，我是 Lassie！第一次使用嗎？完成簡單的綁定只需要三分鐘，就可以享用完整的服務！',
        actions=[
            URIAction(
                label='點我進行綁定',
                uri=app.config['BIND_LINE_LIFF_URL']
            )
        ])
    template_message = TemplateSendMessage(
        alt_text='綁定帳號',
        template=buttons_template
    )
    return template_message

def check_bind_result(email, phone, line_user_id):
    check_result = query_user_data(email, phone, line_user_id)
    return check_result

def query_user_data(email, phone, line_user_id):
    headers = {
        'Account': app.config['SENSOR_LIVE_ACCOUNT'],
        'Authorization': app.config['SENSOR_LIVE_TOKEN']
    }
    data = requests.get(''.join(['https://api.sensor.live/api/projects/', app.config['SENSOR_LIVE_PROJECT_ID'] ,'/end_users/list']), headers=headers)
    query_data = data.json()
    user_items = query_data["items"]
    for user_item in user_items:
        if user_item['email'] == email and user_item['phone'] == phone:
            if not check_line_user_id_exist(user_item['username']):
                bind_line_user_id(user_item['username'], line_user_id)
                return 'success'
            return 'fail: User has been registered'
    return 'fail: User not found'

def check_line_user_id_exist(username):
    database = connect()
    cursor = database.cursor()
    args = (username,)
    cursor.execute("SELECT line_user_id FROM users WHERE aws_username =  %s", args)
    result = cursor.fetchone()
    if result:
        return True
    return False

def bind_line_user_id(username, line_user_id):
    database = connect()
    cursor = database.cursor()
    args = (line_user_id, username,datetime.datetime.now())
    cursor.execute("INSERT INTO users(line_user_id, aws_username, created_at) VALUES (%s,%s,%s)", args)
    database.commit()
    database.close()
