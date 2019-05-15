import datetime
import json

import requests
from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            CarouselContainer, FlexSendMessage,
                            PostbackAction, SeparatorComponent, TextComponent, TextSendMessage,ImageSendMessage)

from ..models import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def summary(thing_id):
    things_shadow_json = get_shadow(thing_id)
    bubble_template_columns = []
    message_list = []
    surv_for_cam = []
    for thing_name in things_shadow_json['state']['reported']['errs']:
        if not thing_name.startswith("cam"):
            if 'h' and 'l' in things_shadow_json['state']['reported'][thing_name]['r']:
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
                            text=''.join([things_shadow_json['state']['reported'][thing_name]['v'] ,  '［' ,
                                 things_shadow_json['state']['reported'][thing_name]['r']['l'] ,  '～'
                                 ,  things_shadow_json['state']['reported'][thing_name]['r']['h'] ,  '］']),
                            flex=0,
                            color='#555555',
                            margin='md',
                            align='end'
                        ),

                    ]
                )
                bubble_template_columns.append(message)
            else:
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
                            text=''.join([things_shadow_json['state']['reported'][thing_name]['v'], '［'
                                 ,  things_shadow_json['state']['reported'][thing_name]['r'] ,  '］']),
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

                if 'h' and 'l' in things_shadow_json['state']['reported'][thing_name][surv]['r']:
                    surv_message = BoxComponent(
                        layout='horizontal',
                        flex=1,
                        spacing='sm',
                        margin='md',
                        contents=[
                            TextComponent(
                                text=things_shadow_json['state']['reported']
                                                [thing_name][surv]['rn'],
                                color='#42659a',
                                margin='md',
                                wrap=True,
                                action=PostbackAction(label=things_shadow_json['state']['reported']
                                [thing_name][surv]['rn'],data=','.join(
                                        [
                                            'get_abnormal_pic',
                                            things_shadow_json['state']['reported']
                                            [thing_name][surv]['url']
                                        ]
                                    )
                                ),
                            ),
                            TextComponent(
                                text=''.join([things_shadow_json['state']['reported']
                                                [thing_name][surv]['v'] , '［' ,  things_shadow_json['state']['reported']
                                                [thing_name][surv]['r']['l'], '～', things_shadow_json['state']['reported']
                                                [thing_name][surv]['r']['h'], '］']),
                                flex=0,
                                color='#555555',
                                margin='md',
                                align='end',
                                wrap=True

                            ),
                        ]
                    )
                    surv_for_cam.append(surv_message)
                else:
                    surv_message = BoxComponent(
                        layout='horizontal',
                        flex=1,
                        spacing='sm',
                        margin='md',
                        contents=[
                            TextComponent(
                                text=things_shadow_json['state']['reported']
                                [thing_name][surv]['rn'],
                                color='#42659a',
                                margin='md',
                                action=PostbackAction(label=things_shadow_json['state']['reported']
                                [thing_name][surv]['rn'], data=','.join(
                                        [
                                            'get_abnormal_pic',
                                            things_shadow_json['state']['reported']
                                            [thing_name][surv]['url']
                                        ]
                                    )
                                ),
                                wrap=True
                            ),
                            TextComponent(
                                text=''.join([things_shadow_json['state']['reported']
                                [thing_name][surv]['v']['c'] , '［',  things_shadow_json['state']['reported']
                                [thing_name][surv]['v']['t'] ,  "秒", '］']),
                                flex=0,
                                color='#555555',
                                margin='md',
                                align='end',
                                wrap=True
                            ),
                        ]
                    )
                    surv_for_cam.append(surv_message)
            bubble_for_cam = BubbleContainer(
                direction='ltr',
                header=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text='圖片異常總覽',
                            wrap=True,
                            color='#1DB446',
                            size='xxl',
                            weight='bold',
                            margin='md',
                        ),
                        TextComponent(
                            text=things_shadow_json['state']['reported']['n'],
                            size='lg',
                            color='#aaaaaa',
                        ),
                        SeparatorComponent(margin='xl'),
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
                                    text='規則名稱',
                                    weight='bold',
                                    color='#030303',
                                    size='lg'
                                ),
                                TextComponent(
                                    text='數值［規則］',
                                    weight='bold',
                                    color='#030303',
                                    margin='md',
                                    align='end',
                                    size='lg'
                                )
                            ]
                        ),
                        SeparatorComponent(margin='xl'),
                        BoxComponent(
                            layout='vertical',
                            flex=1,
                            spacing='sm',
                            margin='md',
                            contents=surv_for_cam
                        ),
                        SeparatorComponent(margin='xl'),
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
                                    text=(datetime.datetime.now() +
                                          datetime.timedelta(hours=0)).strftime(
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
                )
            )
            message = FlexSendMessage(
                alt_text='異常總表',
                contents=bubble_for_cam
            )
            message_list.append(message)
    bubble = BubbleContainer(
        direction='ltr',
        header=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                    text='異常總覽',
                    wrap=True,
                    color='#1DB446',
                    size='xxl',
                    weight='bold',
                    margin='md',
                ),
                TextComponent(
                    text=things_shadow_json['state']['reported']['n'],
                    size='lg',
                    color='#aaaaaa',
                ),
                SeparatorComponent(margin='xl'),
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
                            text='數值［規則］',
                            weight='bold',
                            color='#030303',
                            margin='md',
                            align='end',
                            size='lg'
                            )
                        ]
                    ),
                SeparatorComponent(margin='xl'),
                BoxComponent(
                    layout='vertical',
                    flex=1,
                    spacing='sm',
                    margin='md',
                    contents=bubble_template_columns
                ),
                SeparatorComponent(margin='xl'),
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
            'projects/',
            app.config['SENSOR_LIVE_PROJECT_ID'],
            '/things/',
            thing_id,
            '/shadow'
        ]),
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
    if devices_data:
        message = have_alarm_message(devices_data)
        message_list.append(message)
    else:
        message = no_alarm_message()
        message_list.append(message)
    return message_list

def get_abnormal_pic(url):
    """Get abnormal picture from alarm list message

    :param str url: url for the picture url
    """
    message = ImageSendMessage(
            preview_image_url=str(url),
            original_content_url=str(url)
        )
    return message



def have_alarm_message(devices_data):
    carousel_template_columns = []
    for device_data in devices_data:
        things_shadow = requests.get(
            ''.join([
                app.config['SENSOR_LIVE_API_URL'],
                'projects/',
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
        if things_shadow_json is not None:
            if things_shadow_json['state']['reported']['errs'] != []:
                bubble_template = BubbleContainer(
                    body=BoxComponent(
                        layout='vertical',
                        contents=[
                            TextComponent(
                                text=str(things_shadow_json['state']['reported']['n']),
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

            thing_data.append(
                {
                    'name': thing['name']
                }
            )
        return thing_data
    else:
        return []

