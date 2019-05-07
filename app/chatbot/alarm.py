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
    alarm_value = ''
    alarm_time = time.localtime(int(mqtt_message['timestamp']))
    if mqtt_message['sensorType'] == 'counter':
        unit = ' (次)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rule']),
            ' 次'
        ])
        alarm_value = mqtt_message['value']
    elif (mqtt_message['sensorType'] == 'lamp') or (mqtt_message['sensorType'] == 'detector'):
        unit = ' (偵測值)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rule'])
        ])
        alarm_value = mqtt_message['value']
    elif mqtt_message['sensorType'] == 'current':
        unit = ' (mAh)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rules']['low']),
            " ～ ",
            str(mqtt_message['rules']['high']),
            ' mAh'
        ])
        alarm_value = mqtt_message['value']
    elif mqtt_message['sensorType'] == 'temperature':
        unit = ' (℃)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rules']['low']),
            " ～ ",
            str(mqtt_message['rules']['high']),
            ' ℃'
        ])
        alarm_value = mqtt_message['value']
    elif mqtt_message['sensorType'] == 'humidity':
        unit = ' (%)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rules']['low']),
            " ～ ",
            str(mqtt_message['rules']['high']),
            ' %'
        ])
        alarm_value = mqtt_message['value']
    elif mqtt_message['sensorType'] == 'timer':
        unit = ' (秒)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rule']),
            ' 秒'
        ])
        alarm_value = mqtt_message['value']
    elif mqtt_message['sensorType'] == 'ocr':
        unit = '(偵測值)'
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rules']['low']),
            " ～ ",
            str(mqtt_message['rules']['high']),
        ])
        alarm_value = mqtt_message['value']
        message = ImageSendMessage(
            original_content_url=str(mqtt_message['url']),
            preview_image_url=str(mqtt_message['url'])
        )
        message_list.append(message)
    elif mqtt_message['sensorType'] == 'color':
        unit = ''
        rule = ''.join([
            '設定 : ',
            str(mqtt_message['rules']['color']),
            " 持續 ",
            str(mqtt_message['rules']['high']),
            ' 秒'
        ])
        alarm_value = str(mqtt_message['values']['color'] +
                          ' ' + mqtt_message['values']['time'] + '秒')
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
                                        text=str(alarm_value) + unit,
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
