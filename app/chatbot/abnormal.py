import datetime
import json

import requests
from flask import Flask
from linebot import LineBotApi
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            CarouselContainer, FlexSendMessage,
                            ImageSendMessage, PostbackAction,
                            SeparatorComponent, TextComponent, TextSendMessage)

import config

from ..models import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])


def summary(line_user_id,postback_data):
    user = User.query.filter_by(
        line_user_id=line_user_id
    ).first()
    things_shadow = requests.get(
        ''.join([
            'https://api.sensor.live/api/projects/',
            app.config['SENSOR_LIVE_PROJECT_ID'],
            '/things/',
            postback_data[1],
            '/shadow'
        ]),
        headers={
            'Account': app.config['SENSOR_LIVE_ACCOUNT'],
            'Authorization': app.config['SENSOR_LIVE_TOKEN']
        }
    )
    things_shadow_json = json.loads(things_shadow.text)
    bubble_template_columns = []
    for thing_name in things_shadow_json['state']['reported']['errs']:
        if thing_name.startswith("cam") != 1:
            list = BoxComponent(
                layout='horizontal',
                flex=1,
                spacing='sm',
                margin='md',
                contents=[
                    TextComponent(
                        text=things_shadow_json['state']['reported'][thing_name]['n'],
                        color='#555555',
                        margin='md'
                    ),
                    TextComponent(
                        text=things_shadow_json['state']['reported'][thing_name]['v'],
                        flex=0,
                        color='#555555',
                        margin='md',
                        align='end'
                    ),

                ]
            )
            bubble_template_columns.append(list)
        else:
            for surv in things_shadow_json['state']['reported'][thing_name]['errs']:
                bubble_for_cam = BubbleContainer(
                    direction='ltr',
                    header=BoxComponent(
                        layout='vertical',
                        contents=[
                            TextComponent(
                                text='Camera Report',
                                wrap=True,
                                color='#1DB446',
                                size='xxl',
                                weight='bold',
                                margin='md',
                            ),
                            TextComponent(
                                text=things_shadow_json['state']['reported']['n'],
                                size='xs',
                                color='#aaaaaa',
                            ),
                            SeparatorComponent(),
                        ],
                    ),
                    body=BoxComponent(
                        layout='vertical',
                        flex=1,
                        spacing='sm',
                        margin='md',
                        contents=[
                            BoxComponent(
                                layout='horizontal',
                                flex=1,
                                spacing='sm',
                                margin='md',
                                contents=[
                                    TextComponent(
                                        text='Sensor',
                                        weight='bold',
                                        color='#030303',
                                        size='lg'
                                    ),
                                    TextComponent(
                                        text='Value',
                                        weight='bold',
                                        color='#030303',
                                        margin='md',
                                        align='end',
                                        size='lg'
                                    )
                                ]
                            ),
                            SeparatorComponent(),
                            BoxComponent(
                                layout='vertical',
                                flex=1,
                                spacing='sm',
                                margin='md',
                                contents=[
                                    BoxComponent(
                                        layout='horizontal',
                                        flex=1,
                                        spacing='sm',
                                        margin='md',
                                        contents=[
                                            TextComponent(
                                                text=things_shadow_json['state']['reported'][thing_name][surv]['n'],
                                                color='#555555',
                                                margin='md'
                                            ),
                                            TextComponent(
                                                text=things_shadow_json['state']['reported'][thing_name][surv]['v'],
                                                flex=0,
                                                color='#555555',
                                                margin='md',
                                                align='end'
                                            ),

                                        ]
                                    )
                                ]
                            ),
                            SeparatorComponent(),
                            BoxComponent(
                                layout='horizontal',
                                flex=1,
                                spacing='sm',
                                margin='md',
                                contents=[
                                    TextComponent(
                                        text='Date',
                                        weight='regular',
                                        align='start',
                                        color='#aaaaaa',
                                        size='xs',
                                        gravity="top"
                                    ),
                                    TextComponent(
                                        text=(datetime.datetime.now() + datetime.timedelta(hours=0)).strftime(
                                            '%Y-%m-%d %H:%M:%S'),
                                        weight='regular',
                                        color='#aaaaaa',
                                        margin='md',
                                        align='end',
                                        size='xs',
                                        gravity="top"
                                    ),

                                ]
                            ),

                        ]
                    ),

                )
                line_bot_api.push_message(line_user_id, FlexSendMessage(alt_text='異常總表', contents=bubble_for_cam))
                line_bot_api.push_message(line_user_id, ImageSendMessage(original_content_url=str(things_shadow_json['state']['reported'][thing_name][surv]['url']),
                                                                         preview_image_url=str(things_shadow_json['state']['reported'][thing_name][surv]['url'])))
    bubble = BubbleContainer(
        direction='ltr',
        header=BoxComponent(
            layout='vertical',
            contents=[
               TextComponent(
                    text='Report',
                    wrap=True,
                    color='#1DB446',
                    size='xxl',
                    weight='bold',
                    margin='md',
                ),
               TextComponent(
                    text=postback_data[1],
                    size='xs',
                    color='#aaaaaa',
                ),
               SeparatorComponent(),
            ],
        ),
        body=BoxComponent(
            layout='vertical',
            flex=1,
            spacing='sm',
            margin='md',
            contents=[
                BoxComponent(
                    layout='horizontal',
                    flex=1,
                    spacing='sm',
                    margin='md',
                    contents=[
                TextComponent(
                    text='Sensor',
                    weight='bold',
                    color='#030303',
                    size='lg'
                    ),
                TextComponent(
                    text='Value',
                    weight='bold',
                    color='#030303',
                    margin='md',
                    align='end',
                    size='lg'
                    )
                ]
            ),
                SeparatorComponent(),
                BoxComponent(
                    layout='vertical',
                    flex=1,
                    spacing='sm',
                    margin='md',
                    contents=bubble_template_columns
                ),
                SeparatorComponent(),
                BoxComponent(
                    layout='horizontal',
                    flex=1,
                    spacing='sm',
                    margin='md',
                    contents=[
                        TextComponent(
                            text='Date',
                            weight='regular',
                            align='start',
                            color='#aaaaaa',
                            size='xs',
                            gravity="top"
                        ),
                        TextComponent(
                            text=(datetime.datetime.now() + datetime.timedelta(hours=0)).strftime(
                                '%Y-%m-%d %H:%M:%S'),
                            weight='regular',
                            color='#aaaaaa',
                            margin='md',
                            align='end',
                            size='xs',
                            gravity="top"
                        ),

                    ]
                ),

            ]
        ),

    )
    message = FlexSendMessage(alt_text='異常總表', contents=bubble)
    return message


def device_list_message_for_alarmlist(line_user_id):
    devices_data = get_device_list_data_for_alarmlist(line_user_id)
    if devices_data:
        line_bot_api.push_message(line_user_id, TextSendMessage(text="搜尋異常萊西中..."))
        return have_device_message_for_alarmlist(line_user_id, devices_data)
    else:
        return no_device_message_for_alarmlist(line_user_id)

def have_device_message_for_alarmlist(line_user_id, devices_data):
    carousel_template_columns = []
    for device_data in devices_data:
        things_shadow = requests.get(
            ''.join([
                'https://api.sensor.live/api/projects/',
                app.config['SENSOR_LIVE_PROJECT_ID'],
                '/things/',
                device_data['name'],
                '/shadow'
            ]),
            headers={
                'Account': app.config['SENSOR_LIVE_ACCOUNT'],
                'Authorization': app.config['SENSOR_LIVE_TOKEN']
            }
        )
        things_shadow_json = json.loads(things_shadow.text)
        if things_shadow_json is None:
            pass
        elif things_shadow_json !={}:
            if things_shadow_json['state']['reported']['errs'] !=[]:
                bubble_template = BubbleContainer(
                    body=BoxComponent(
                        layout='vertical',
                        contents=[
                            TextComponent(
                                text=str(device_data['display_name']),
                                wrap=True,
                                weight='bold',
                                size='lg',
                            ),
                            ButtonComponent(
                                action=PostbackAction(label="異常總表", data=','.join(['abnormal',device_data['name']]),display_text='正在傳送...'),
                                flex=100,
                                size='xl',
                                weight='bold',
                                height='sm',
                                gravity='center',
                                style='link'
                            ),
                        ]
                    )
                )
                carousel_template_columns.append(bubble_template)

    if carousel_template_columns == []:
        line_bot_api.push_message(line_user_id, TextSendMessage(text='未偵測到異常萊西！！'))
    else:
        message = FlexSendMessage(
            alt_text='異常設備清單',
            contents=CarouselContainer(
                contents=carousel_template_columns
            )
        )
        line_bot_api.push_message(line_user_id, message)
def no_device_message_for_alarmlist(line_user_id):
    line_bot_api.push_message(
        line_user_id,
        TextSendMessage(
            text='搜尋不到任何萊西！'
        )
    )

def get_device_list_data_for_alarmlist(line_user_id):
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
            thing_data.append(
                {
                    'name': thing_response_json['name'],
                    'display_name': thing_response_json['display_name']
                }
            )
        return thing_data
    else:
        return []
