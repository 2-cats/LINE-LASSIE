import urllib

from flask import Flask
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            FlexSendMessage, IconComponent, ImageComponent,
                            ImageSendMessage, SeparatorComponent,
                            TextComponent, URIAction)

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def lassie_report(mqtt_message):
    return lassie_report_message(mqtt_message['d'])
    

def lassie_report_message(data):
    message = FlexSendMessage(
        alt_text='今日報表',
        contents=BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                flex=1,
                spacing='md',
                margin='md',
                contents=[
                    TextComponent(
                        text='今日報表',
                        weight='bold',
                        size='lg',
                        color='#1DB446'
                    ),
                    TextComponent(
                        text='我已經幫你把今日報表整理完成了，請點擊檢視',
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
                            uri=''.join([
                               app.config['REPORT_LINE_LIFF_URL'],
                               "?data=",
                               urllib.parse.quote_plus(str(data)) 
                            ])
                        )
                    )
                ]
            )
        )
    )
    return message
