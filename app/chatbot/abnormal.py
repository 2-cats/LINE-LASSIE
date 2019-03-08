import datetime
import json

import requests
from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            CarouselContainer, FlexSendMessage,
                            ImageSendMessage, PostbackAction,
                            SeparatorComponent, TextComponent, TextSendMessage)

from ..models import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def summary(thing_id):
    things_shadow_json = get_shadow(thing_id)
    bubble_template_columns = []
    message_list = []
    for thing_name in things_shadow_json['state']['reported']['errs']:
        if not thing_name.startswith("cam"):
            message = BoxComponent(
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
            bubble_template_columns.append(message)
        else:
            for surv in things_shadow_json['state']['reported'][thing_name]['errs']:
                bubble_for_cam = BubbleContainer(
                    direction='ltr',
                    header=BoxComponent(
                        layout='vertical',
                        contents=[
                            TextComponent(
                                text='圖片報告',
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
                                        text='感測器',
                                        weight='bold',
                                        color='#030303',
                                        size='lg'
                                    ),
                                    TextComponent(
                                        text='數值',
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
                                        text='日期',
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
                                        gravity="top",
                                        flex=5
                                    ),

                                ]
                            ),

                        ]
                    ),

                )
                message = FlexSendMessage(
                    alt_text='異常總表',
                    contents=bubble_for_cam
                )
                message_list.append(message)
                message = ImageSendMessage(
                    original_content_url=str(things_shadow_json['state']['reported'][thing_name][surv]['url']),
                    preview_image_url=str(things_shadow_json['state']['reported'][thing_name][surv]['url'])
                )
                message_list.append(message)
    
    bubble = BubbleContainer(
        direction='ltr',
        header=BoxComponent(
            layout='vertical',
            contents=[
               TextComponent(
                    text='報告',
                    wrap=True,
                    color='#1DB446',
                    size='xxl',
                    weight='bold',
                    margin='md',
                ),
               TextComponent(
                    text=thing_id,
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
                    text='感測器',
                    weight='bold',
                    color='#030303',
                    size='lg'
                    ),
                TextComponent(
                    text='數值',
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
                            text='日期',
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
                            gravity="top",
                            flex=5
                        ),

                    ]
                ),

            ]
        ),

    )
    message = FlexSendMessage(
        alt_text='異常總表',
        contents=bubble
    )
    message_list.append(message)
    return message_list

def get_shadow(thing_id):
    # Get things shadow
    things_shadow = requests.get(
        ''.join([
            app.config['SENSOR_LIVE_API_URL'],
            'projects/{project}/things/{thing}/shadow'
        ]),
        params={
            'porject': app.config['SENSOR_LIVE_PROJECT_ID'],
            'thing': thing_id
        },
        headers={
            'Account': app.config['SENSOR_LIVE_ACCOUNT'],
            'Authorization': app.config['SENSOR_LIVE_TOKEN']
        }
    )
    things_shadow_json = json.loads(things_shadow.text)
    return things_shadow_json

def alarm_list_message(line_user_id):
    devices_data = get_alarm_list_data(line_user_id)
    message_list = []
    print (devices_data)
    if devices_data:
        message = have_alarm_message(devices_data)
        message_list.append(message)
    else:
        message = no_alarm_message()
        message_list.append(message)
    return message_list

def have_alarm_message(devices_data):
    carousel_template_columns = []
    for device_data in devices_data:
        things_shadow = requests.get(
            ''.join([
                app.config['SENSOR_LIVE_API_URL'],
                'projects/{project}/things/{thing}/shadow'
            ]),
            params={
                'porject': app.config['SENSOR_LIVE_PROJECT_ID'],
                'thing':  device_data['name']
            },
            headers={
                'Account': app.config['SENSOR_LIVE_ACCOUNT'],
                'Authorization': app.config['SENSOR_LIVE_TOKEN']
            }
        )
        things_shadow_json = json.loads(things_shadow.text)
        if things_shadow_json is not None:
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
                                action=PostbackAction(
                                    label="異常總表",
                                    data=','.join(
                                        [
                                            'abnormal',
                                            device_data['name']
                                        ]
                                    ),
                                    display_text='查詢異常總覽...'
                                ),
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
        message = TextSendMessage(text='未偵測到異常萊西！！')
    else:
        message = FlexSendMessage(
            alt_text='異常設備清單',
            contents=CarouselContainer(
                contents=carousel_template_columns
            )
        )
    return message

def no_alarm_message():
    message = TextSendMessage(
        text='搜尋不到任何萊西！'
    )
    return message

def get_alarm_list_data(line_user_id):
    user = User.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()

    things_response = requests.get(
        ''.join([
            app.config['SENSOR_LIVE_API_URL'],
            'projects/{project}/end_users/{end_user_username}/resources?target=things',
        ]),
        params={
            'porject': app.config['SENSOR_LIVE_PROJECT_ID'],
            'end_user_username': user.aws_user_name
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
                ''.join([
                    app.config['SENSOR_LIVE_API_URL'],
                    'projects/{porject}/things/{thing}'
                ]),
                params={
                    'porject': app.config['SENSOR_LIVE_PROJECT_ID'],
                    'thing': thing['name']
                },
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
