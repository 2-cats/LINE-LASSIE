import datetime
import json

import requests
from flask import Flask
from linebot import LineBotApi
from linebot.models import (BoxComponent, BubbleContainer, CarouselContainer,
                            FlexSendMessage, TextComponent, TextSendMessage)

import config

from ..models import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])

def device_list_message(line_user_id):
    devices_data = get_device_list_data(line_user_id)
    if devices_data:
        line_bot_api.push_message(
            line_user_id,
            have_device_message(line_user_id, devices_data)
        ) 
    else:
        line_bot_api.push_message(
            line_user_id,
            no_device_message(line_user_id)
        )

def have_device_message(line_user_id, devices_data):
    carousel_template_columns = []
    for device_data in devices_data:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text=str(device_data['name']),
                        wrap=True,
                        weight= 'bold',
                        size='lg',
                    ),
                    TextComponent(
                        text=str(device_data['device_status']),
                        wrap=True,
                        size='sm',
                        margin='md',
                        color=device_data['text_color']
                    )
                ]
            )
        )
        carousel_template_columns.append(bubble_template)
    message = FlexSendMessage(
        alt_text='您的設備清單',
        contents=CarouselContainer(
            contents=carousel_template_columns
        )
    )
    return message

def no_device_message(line_user_id):
    return TextSendMessage(
            text='您尚未使用任何萊西！'
        )

def get_device_list_data(line_user_id):
    user = User.query.filter_by(
        line_user_id=line_user_id
    ).first()
    things_response = requests.get(
        ''.join([
            'https://api.sensor.live/api/projects/',
            app.config['SENSOR_LIVE_PROJECT_ID'],
            '/end_users/',
            '54ce49c7-9fc0-482d-850c-a39ae37f0d6c',
            '/resources?target=things'
        ]),
        headers={
            'Account': app.config['SENSOR_LIVE_ACCOUNT'],
            'Authorization': app.config['SENSOR_LIVE_TOKEN']
        }
    )
    if things_response.status_code == 200:
        thing_data = []
        things_response_json = json.loads(things_response.text)
        for thing in things_response_json['data']:
            thing_response = requests.get(
                ''.join([
                    'https://api.sensor.live/api/projects/',
                    app.config['SENSOR_LIVE_PROJECT_ID'],
                    '/things/',
                    thing['name']
                ]),
                headers={
                    'Account': app.config['SENSOR_LIVE_ACCOUNT'],
                    'Authorization': app.config['SENSOR_LIVE_TOKEN']
                }
            )
            thing_response_json = json.loads(thing_response.text)
            updated_at = datetime.datetime.strptime(thing_response_json['updated_at'], '%Y-%m-%d %H:%M:%S')
            updated_at_timedelta = updated_at + datetime.timedelta(seconds=thing_response_json['keep_alive'])  
            alive = '離線'
            text_color = '#FF3333'
            if datetime.datetime.now() < updated_at_timedelta:
                alive = '連接中'
                text_color = '#1DB446'
            thing_data.append(
                {
                    'name': thing_response_json['display_name'],
                    'device_status': alive,
                    'text_color': text_color
                }
            )
        return thing_data
    else:
        return []
