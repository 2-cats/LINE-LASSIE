import datetime
import json

import requests
from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, CarouselContainer,
                            FlexSendMessage, TextComponent, TextSendMessage)

from ..models import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def device_list_message(line_user_id):
    # Get device data
    devices_data = get_device_list_data(line_user_id)
    # If user have device data
    if devices_data:
        message = have_device_message(devices_data)
    # If user not have device data
    else:
        message = no_device_message()
    return message

def have_device_message(devices_data):
    carousel_template_columns = []

    # Use device_data into LINE message template
    for device_data in devices_data:
        bubble_template = BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text=str(device_data['name']),
                        wrap=True,
                        weight='bold',
                        size='lg',
                    )
                ]
            ),
            footer=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text=str(device_data['name']),
                        wrap=True,
                        weight='bold',
                        size='lg',
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

def no_device_message():
    return TextSendMessage(text='您尚未使用任何萊西！')

def get_device_list_data(line_user_id):
    # Query user data
    user = User.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()
    # Query enduser resources
    things_response = requests.get(
        ''.join([
            app.config['SENSOR_LIVE_API_URL'],
            'projects/',
            app.config['SENSOR_LIVE_PROJECT_ID'],
            '/end_users/',
            user.aws_user_name,
            '/resources'
        ]),
        params={
            'target': 'things'
        },
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
                ''.join(
                    [
                        app.config['SENSOR_LIVE_API_URL'],
                        'projects/',
                        str(app.config['SENSOR_LIVE_PROJECT_ID']),
                        '/things/',
                        thing['name']
                    ]
                ),
                headers={
                    'Account': app.config['SENSOR_LIVE_ACCOUNT'],
                    'Authorization': app.config['SENSOR_LIVE_TOKEN']
                }
            )
            thing_response_json = json.loads(thing_response.text)
        return thing_data
    return []
