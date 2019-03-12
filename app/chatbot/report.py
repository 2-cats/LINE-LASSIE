import urllib

import requests
from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            FlexSendMessage, TextComponent, TextSendMessage,
                            URIAction)

from ..models import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')


def make_report_message(mqtt, line_user_id):
    user = User.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()
    if user:
        content = '好的，我正在為你準備報表，請稍候'
        topic = ''.join(
            [
                '/lassie/',
                user.aws_user_name,
                '/getTodayReport'
            ]
        )
        mqtt.publish(topic, '')
    else:
        content = '錯誤的指令'
    return TextSendMessage(text=content)

def lassie_report_message(mqtt_message):
    thing_name = mqtt_message['x']
    data = mqtt_message['d']
    message = FlexSendMessage(
        alt_text=''.join([thing_name, ' 的今日報表']),
        contents=BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                flex=1,
                spacing='md',
                margin='md',
                contents=[
                    TextComponent(
                        text=''.join([thing_name, ' 的今日報表']),
                        wrap=True,
                        weight='bold',
                        size='lg',
                        color='#1DB446'
                    ),
                    TextComponent(
                        text='我已經幫你整理完成了，請點擊檢視',
                        wrap=True,
                        size='md',
                    )
                ]
            ),
            footer=BoxComponent(
                layout='vertical',
                flex=1,
                spacing='md',
                margin='md',
                contents=[
                    ButtonComponent(
                        style='link',
                        action=URIAction(
                            label='檢視報表',
                            uri=''.join(
                                [
                                    app.config['REPORT_LINE_LIFF_URL'],
                                    "?data=",
                                    urllib.parse.quote_plus(str(data))
                                ]
                            )
                        )
                    )
                ]
            )
        )
    )
    return message
