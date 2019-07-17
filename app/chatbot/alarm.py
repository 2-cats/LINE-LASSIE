import time
from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, FlexSendMessage,
                            ImageComponent, ImageSendMessage, SeparatorComponent,
                            TextComponent)


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def lassie_alarm_message(mqtt_message):
    message_list = []
    unit = ''
    rule = ''
    sensor_type = mqtt_message['sensorType']
    alarm_time = time.localtime(int(mqtt_message['timestamp']/1000))
    if sensor_type == 'counter':
        unit = ' (次)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rule']),
            ' 次'
        ])
    elif (sensor_type == 'lamp') or (sensor_type == 'detector'):
        unit = ' (偵測值)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rule'])
        ])
    elif sensor_type == 'current':
        unit = ' (mAh)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rules']['low']),
            " ～ ",
            str(mqtt_message['rules']['high']),
            ' mAh'
        ])
    elif sensor_type == 'temperature':
        unit = ' (℃)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rules']['low']),
            " ～ ",
            str(mqtt_message['rules']['high']),
            ' ℃'
        ])
    elif sensor_type == 'humidity':
        unit = ' (%)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rules']['low']),
            " ～ ",
            str(mqtt_message['rules']['high']),
            ' %'
        ])
    elif sensor_type == 'timer':
        unit = ' (秒)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rule']),
            ' 秒'
        ])
    elif sensor_type == 'ocr':
        unit = '(偵測值)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rules']['low']),
            " ～ ",
            str(mqtt_message['rules']['high']),
        ])
        message = ImageSendMessage(
            original_content_url=str(mqtt_message['url']),
            preview_image_url=str(mqtt_message['url'])
        )
        message_list.append(message)
    elif sensor_type == 'color':
        unit = ''
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rules']['color']),
            " 持續 ",
            str(mqtt_message['rules']['high']),
            ' 秒'
        ])

        message = ImageSendMessage(
            original_content_url=str(mqtt_message['url']),
            preview_image_url=str(mqtt_message['url'])
        )
        message_list.append(message)

    message = FlexSendMessage(
        alt_text='異常通知',
        contents=BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                flex=1,
                spacing='md',
                margin='md',
                contents=[
                    TextComponent(
                        text=mqtt_message['thingDisplayName'] + ' 異常',
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
                                        text=mqtt_message['sensorDisplayName'],
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
                                        text=str(mqtt_message['value']) + unit,
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
                        text=time.strftime('%Y-%m-%d %H:%M:%S', alarm_time),
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
