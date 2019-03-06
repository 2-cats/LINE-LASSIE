import urllib

import pymysql
from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            FlexSendMessage, IconComponent, ImageComponent,
                            ImageSendMessage, SeparatorComponent,
                            TextComponent, URIAction)

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def lassie_alarm_message(mqtt_message):
    unit = ''
    rule = ''
    if mqtt_message['t'] == 'counter':
        unit = ' (次)'
        rule = '設定 : ' + str(mqtt_message['r']) + ' 次'
    elif (mqtt_message['t'] == 'lamp') or ( mqtt_message['t'] == 'state') or (mqtt_message['t'] == 'color') or (mqtt_message['t'] == 'detector'):
        unit = ' (偵測值)'
        rule = '設定 : ' + str(mqtt_message['r'])
    elif mqtt_message['t'] == 'current':
        unit = ' (mAh)'
        rule = '設定 : ' + str(mqtt_message['r']) + ' mAh'
    elif mqtt_message['t'] == 'temperature':
        unit = ' (℃)'
        rule = '設定 : ' + str(mqtt_message['ra']['h']) + " ～ " + str(mqtt_message['ra']['l']) + ' ℃'
    elif mqtt_message['t'] == 'humidity':
        unit = ' (%)'
        rule = '設定 : ' + str(mqtt_message['ra']['h']) + " ～ " + str(mqtt_message['ra']['l']) + ' %'
    elif mqtt_message['t'] == 'timer':
        unit = ' (秒)'
        rule = '設定 : ' + str(mqtt_message['r']) + ' 秒'
    elif mqtt_message['t'] == 'ocr':
        unit = '(偵測值)'
        rule = '設定 : ' + str(mqtt_message['ra']['h']) + " ～ " + str(mqtt_message['ra']['l'])
    message_list = []
    if mqtt_message['url'] != "":
        message = ImageSendMessage(
            original_content_url=str(mqtt_message['url']),
            preview_image_url=str(mqtt_message['url'])
        )
        message_list.append(message)
    message = FlexSendMessage(
        alt_text='異常通知',
        contents=BubbleContainer(
             hero=ImageComponent(
                 url='https://i.imgur.com/GIrEMgY.png',
                 size='full',
                 aspect_ratio='20:13',
                 aspect_mode='cover'
             ),
            body=BoxComponent(
                layout='vertical',
                flex=1,
                spacing='md',
                margin='md',
                contents=[
                    TextComponent(
                        text=mqtt_message['nt'] + ' 異常',
                        weight='bold',
                        wrap=True,
                        size='xl',
                        color='#464646',
                        flex=1,
                        margin='none',
                        align='center',
                        gravity='top'
                    ),
                    BoxComponent(
                        layout='vertical',
                        flex=1,
                        spacing='sm',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                flex=1,
                                spacing='sm',
                                margin='md',
                                contents=[

                                    TextComponent(
                                        text=mqtt_message['ns'],
                                        weight='bold',
                                        wrap=True,
                                        size='md',
                                        color='#464646',
                                        flex=0,
                                        margin='sm',
                                        align='start',
                                        gravity='top'
                                    ),
                                    TextComponent(
                                        text=str(mqtt_message['v']) + unit,
                                        weight='bold',
                                        wrap=False,
                                        size='xl',
                                        color='#D0021B',
                                        flex=1,
                                        margin='md',
                                        align='end',
                                        gravity='top'
                                    ),
                                ]
                            )
                        ]
                    ),
                    TextComponent(
                        text=str(rule),
                        weight='regular',
                        wrap=True,
                        size='sm',
                        color='#000000',
                        flex=1,
                        margin='md',
                        align='end',
                        gravity='top'
                    ),
                    SeparatorComponent(),
                    TextComponent(
                        text=mqtt_message['time'],
                        weight='regular',
                        wrap=True,
                        size='xs',
                        color='#aaaaaa',
                        flex=1,
                        margin='sm',
                        align='end',
                        gravity='top'
                    ),

                ]
            )
        )
    )
    message_list.append(message)
    return message_list

def get_push_id(username):
    database = pymysql.connect(
        app.config['DB_HOST'],
        app.config['DB_USERNAME'],
        app.config['DB_PASSWORD'],
        app.config['DB_NAME'],
        charset="utf8"
    )
    cursor = database.cursor()
    args = (username,)
    cursor.execute("SELECT source_id FROM users JOIN members ON users.id = members.user_id WHERE users.aws_user_name = %s ORDER BY members.id DESC", args)
    member_result = cursor.fetchone()
    if member_result is None:
        cursor.execute("SELECT line_user_id FROM users WHERE aws_user_name = %s", args)
        user_result = cursor.fetchone()
        psuh_id = user_result[0]
    else:
       psuh_id = member_result[0]
    database.close()
    return psuh_id
