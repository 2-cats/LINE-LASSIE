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
    """Get thing data from sensor.live API

    :param str thing_id: thing id
    """
    # Get shadow reported
    things_shadow = get_shadow(thing_id)
    things_reported = things_shadow['state']['reported']

    # Store all message
    message_list = []

    # Store camera surv message
    cam_surv_contents = []

    # Store general surv message
    surv_contents = []

    # Check error thing list
    for thing_name in things_reported['errs']:
        # Check sensor type is camera(cam)
        if thing_name.startswith("cam"):
            for surv in things_reported[thing_name]['errs']:
                # Generate cam surv content component
                # Check key: h and l in rule
                if 'l' in things_reported[thing_name][surv]['r'] and 'h' in things_reported[thing_name][surv]['r']:
                    cam_surv_content = BoxComponent(
                        layout='horizontal',
                        flex=1,
                        spacing='sm',
                        margin='md',
                        contents=[
                            TextComponent(
                                text=things_reported[thing_name][surv]['rn'],
                                color='#42659a',
                                margin='md',
                                wrap=True,
                                action=PostbackAction(
                                    label=things_reported[thing_name][surv]['rn'],
                                    data=','.join(
                                        [
                                            'get_abnormal_pic',
                                            things_reported[thing_name][surv]['eu']
                                        ]
                                    )
                                ),
                            ),
                            TextComponent(
                                text=''.join(
                                    [
                                        things_reported[thing_name][surv]['v'] ,
                                        '［' ,
                                        things_reported[thing_name][surv]['r']['l'],
                                        '～',
                                        things_reported[thing_name][surv]['r']['h'],
                                        '］'
                                    ]
                                ),
                                flex=0,
                                color='#555555',
                                margin='md',
                                align='end',
                                wrap=True
                            ),
                        ]
                    )
                else:
                    cam_surv_content = BoxComponent(
                        layout='horizontal',
                        flex=1,
                        spacing='sm',
                        margin='md',
                        contents=[
                            TextComponent(
                                text=things_reported[thing_name][surv]['rn'],
                                color='#42659a',
                                margin='md',
                                action=PostbackAction(
                                    label=things_reported[thing_name][surv]['rn'],
                                    data=','.join(
                                        [
                                            'get_abnormal_pic',
                                            things_reported[thing_name][surv]['eu']
                                        ]
                                    )
                                ),
                                wrap=True
                            ),
                            TextComponent(
                                text=''.join(
                                    [
                                        things_reported[thing_name][surv]['v']['c'],
                                        '［',
                                        things_reported[thing_name][surv]['r']['c'],
                                        things_reported[thing_name][surv]['r']['h'],
                                        "秒",
                                        '］'
                                    ]
                                ),
                                flex=0,
                                color='#555555',
                                margin='md',
                                align='end',
                                wrap=True
                            ),
                        ]
                    )
                cam_surv_contents.append(cam_surv_content)

        # Check sensor type is another
        else:
            # Generate surv content component
            # If key 'h' and 'l' in rule.
            if 'h' in things_reported[thing_name]['r'] and 'l' in things_reported[thing_name]['r']:
                surv_content = BoxComponent(
                    layout='horizontal',
                    flex=1,
                    spacing='sm',
                    margin='md',
                    contents=[
                        TextComponent(
                            text=things_reported[thing_name]['n'],
                            color='#555555',
                            margin='md'
                        ),
                        TextComponent(
                            text=''.join(
                                [
                                    things_reported[thing_name]['v'],
                                    '［',
                                    things_reported[thing_name]['r']['l'],
                                    '～',
                                    things_reported[thing_name]['r']['h'],
                                    '］'
                                ]
                            ),
                            flex=0,
                            color='#555555',
                            margin='md',
                            align='end'
                        ),

                    ]
                )
            else:
                surv_content = BoxComponent(
                    layout='horizontal',
                    flex=1,
                    spacing='sm',
                    margin='md',
                    contents=[
                        TextComponent(
                            text=things_reported[thing_name]['n'],
                            color='#555555',
                            margin='md'
                        ),
                        TextComponent(
                            text=''.join(
                                [
                                    things_reported[thing_name]['v'],
                                    '［',
                                    things_reported[thing_name]['r'],
                                    '］'
                                ]
                            ),
                            flex=0,
                            color='#555555',
                            margin='md',
                            align='end'
                        ),

                    ]
                )
            surv_contents.append(surv_content)
    # Genetate cam alarm message
    if cam_surv_contents != []:
        message = FlexSendMessage(
            alt_text='異常總表',
            contents=BubbleContainer(
                direction='ltr',
                header=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text='圖片異常總覽',
                            wrap=True,
                            color='#1DB446',
                            size='xxl',
                            margin='md',
                        ),
                        TextComponent(
                            text=things_reported['n'],
                            size='lg',
                            margin='sm',
                            color='#aaaaaa',
                        ),
                        SeparatorComponent(
                            margin='xl'
                        ),
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
                                    color='#030303',
                                    margin='md',
                                    align='end',
                                    size='lg'
                                )
                            ]
                        ),
                        SeparatorComponent(
                            margin='md'
                        ),
                        BoxComponent(
                            layout='vertical',
                            flex=1,
                            spacing='sm',
                            margin='md',
                            contents=cam_surv_contents
                        ),
                        SeparatorComponent(
                            margin='md'
                        ),
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
        )
        message_list.append(message)

    # Genetate general alarm message
    message = FlexSendMessage(
        alt_text='異常總表',
        contents=BubbleContainer(
            direction='ltr',
            header=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text='異常總覽',
                        wrap=True,
                        color='#1DB446',
                        size='xxl',
                        margin='md',
                    ),
                    TextComponent(
                        text=things_reported['n'],
                        size='lg',
                        margin='sm',
                        color='#aaaaaa',
                    ),
                    SeparatorComponent(
                        margin='xl'
                    ),
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
                                color='#030303',
                                size='lg'
                                ),
                            TextComponent(
                                text='數值［規則］',
                                color='#030303',
                                margin='md',
                                align='end',
                                size='lg'
                                )
                            ]
                        ),
                    SeparatorComponent(
                        margin='xl'
                    ),
                    BoxComponent(
                        layout='vertical',
                        flex=1,
                        spacing='sm',
                        margin='md',
                        contents=surv_contents
                    ),
                    SeparatorComponent(
                        margin='xl'
                    ),
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
    )
    message_list.append(message)
    return message_list

def alarm_list_message(line_user_id):
    """Generate alarm list message
    """
    devices_data = get_resources_data(line_user_id)
    message_list = []
    if devices_data:
        message = have_alarm_message(devices_data)
        message_list.append(message)
    else:
        message = no_alarm_message()
        message_list.append(message)
    return message_list

def have_alarm_message(devices_data):
    """If alarm list data found
    :param str devices_data: thing data
    """
    carousel_template_columns = []
    for device_data in devices_data:

        # Get shadow
        things_shadow = get_shadow(device_data['name'])
        things_reported = things_shadow['state']['reported']

        # Check things_shadow is not none
        if things_shadow is not None:
            # Check things_shadow is not empty array
            if things_reported['errs'] != []:
                # Alarm message
                bubble_template = BubbleContainer(
                    body=BoxComponent(
                        layout='vertical',
                        contents=[
                            TextComponent(
                                text=str(things_reported['n']),
                                wrap=True,
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
                                    display_text=''.join(['查詢 ', device_data['name'] ,' 的異常總覽'])
                                ),
                                style='link'
                            ),
                        ]
                    )
                )
                carousel_template_columns.append(bubble_template)
    # Check have data in carousel_template_columns
    if carousel_template_columns == []:
        message = TextSendMessage(text='太好了！沒有偵測到萊西的異常')
    else:
        message = FlexSendMessage(
            alt_text='異常總覽',
            contents=CarouselContainer(
                contents=carousel_template_columns
            )
        )
    return message

def no_alarm_message():
    """If alarm list data not found anything
    """
    message = TextSendMessage(
        text='搜尋不到任何萊西！'
    )
    return message

def abnormal_pic_message(url):
    """Get abnormal picture from alarm list message

    :param str url: url for the picture url
    """
    message = ImageSendMessage(
            preview_image_url=str(url),
            original_content_url=str(url)
        )
    return message

def get_shadow(thing_id):
    """# Get things shadow

    :param str thing_id: thing id
    """
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
    things_shadow = json.loads(things_shadow.text)
    return things_shadow

def get_resources_data(line_user_id):
    """Get resources data from sensor.live API

    :param str line_user_id: LINE user id
    """

    # Query user from database 
    user = User.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()

    # Get API: projects/{{SENSOR_LIVE_PROJECT_ID}}'/end_users/{{aws_user_name}}'/resources'
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

    # Check API response status_code
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
