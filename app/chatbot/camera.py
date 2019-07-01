import datetime
import json

import requests
from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            CarouselContainer, FlexSendMessage,
                            ImageSendMessage, MessageAction, TextComponent,
                            TextSendMessage)

from .. import db
from ..models import CaptureLog, User

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
                    ButtonComponent(
                    style='link',
                    action=MessageAction(
                        label='擷取',
                        text=''.join([
                            'capture ',
                            device_data['name']
                        ])
                    )
                )
                ]
            )
        )
        carousel_template_columns.append(bubble_template)
    message = FlexSendMessage(
        alt_text='您要擷取哪一台萊西的攝影鏡頭',
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
            thing_data.append(
                {
                    'name': thing_response_json['display_name']
                }
            )
        return thing_data
    return []

# Make camera capture action to MQTT
def make_camera_capture(mqtt, thing_name, line_user_id):
    if check_can_capture(line_user_id):
        save_capture_log(line_user_id)
        user = User.query.filter_by(
            line_user_id=line_user_id,
            deleted_at=None
        ).first()
        if user:
            content = '好的，我馬上為您截圖，請稍候'
            topic = ''.join(
                [
                    '/lassie/',
                    user.aws_user_name,
                    '/getCapture'
                ]
            )
            payload = {
                'tn': thing_name
            }
            mqtt.publish(topic, str(payload))
        else:
            content = '錯誤的指令'
        return TextSendMessage(text=content)
    else:
        message = prohibit_capture()
        return message

# check_can_capture
def check_can_capture(line_user_id):
    now = datetime.datetime.now()
    check_time = now - datetime.timedelta(minutes=1)
    capture_logs_count = CaptureLog.query.filter(
        CaptureLog.source_id==line_user_id,
        CaptureLog.source_type=='user',
        CaptureLog.created_at>=check_time
    ).count()
    if capture_logs_count <= app.config["CAPTURE_LIMIT"]:
        return True
    return False


# Prohibit capture
def prohibit_capture():
    bubble_template = BubbleContainer(
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                    text='錯誤',
                    weight='bold',
                    color='#1DB446',
                    size='lg',
                ),
                TextComponent(
                    text='過度頻繁擷取畫面，請稍後再嘗試！',
                    margin='md',
                    wrap=True,
                    color='#666666',
                    size='md',
                )
            ]
        )
    )
    message = FlexSendMessage(
        alt_text='糟糕，出錯了！', contents=bubble_template)
    return message

# Save use capture log
def save_capture_log(line_user_id):
    capture_log = CaptureLog(
        source_id=line_user_id,
        source_type='user'
    )
    try:
        db.session.add(capture_log)
        db.session.commit()
    except:
        pass

# Sub MQTT message to send lassie capture message
def lassie_capture_message(mqtt_message):
    image_url = mqtt_message['iu']
    message = ImageSendMessage(
        original_content_url=image_url,
        preview_image_url=image_url
    )
    return message
