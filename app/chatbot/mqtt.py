import json
import time

from flask import Flask
from linebot import LineBotApi, WebhookHandler
from linebot.models import (BoxComponent, BubbleContainer, FlexSendMessage,
                            ImageComponent, ImageSendMessage, MessageAction,
                            MessageEvent, TextComponent, TextSendMessage)

import config

from ..models import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

#MQTT
HOST = app.config['MQTT_HOSTNAME']
PORT = app.config['MQTT_PORT']

line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])
# Channel Secret
handler = WebhookHandler(app.config['LINE_CHANNEL_SECRET'])


def lassie_alarm_message(mqtt_message):

    # Convert username to line_user_id
    user = User.query.filter_by(aws_user_name=mqtt_message['u'])
    push_id = user.line_user_id

    line_bot_api.push_message(push_id,
                              FlexSendMessage(alt_text='異常通知', contents=BubbleContainer(

                                  hero=ImageComponent(
                                      url='https://i.imgur.com/EzEglZZ.png',
                                      size='full',
                                      aspect_ratio='20:13',
                                      aspect_mode='fit',
                                      margin='none',
                                  ),
                                  body=BoxComponent(
                                      layout='vertical',
                                      flex=1,
                                      spacing='md',
                                      margin='md',
                                      contents=[
                                          TextComponent(
                                              text=mqtt_message['nt'],
                                              weight='bold',
                                              wrap=False,
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
                                              margin='md',
                                              contents=[
                                                  BoxComponent(
                                                      layout='baseline',
                                                      flex=1,
                                                      spacing='sm',
                                                      margin='md',
                                                      contents=[
                                                          IconComponent(aspect_ratio='1:1', margin='none', size='md',
                                                                        url='https://i.imgur.com/OoRVQey.png'),
                                                          TextComponent(text=mqtt_message['ns'], weight='bold', wrap=False,
                                                                        size='md', color='#464646', flex=0, margin='sm',
                                                                        align='start', gravity='top'),
                                                          TextComponent(text=mqtt_message['v'], weight='regular', wrap=False,
                                                                        size='sm', color='#000000', flex=1,
                                                                        margin='none', align='end', gravity='top'),
                                                      ]
                                                  )
                                              ]
                                          ),
                                          TextComponent(
                                              text=mqtt_message['time'],
                                              weight='regular',
                                              wrap=True,
                                              size='xxs',
                                              color='#aaaaaa',
                                              flex=1,
                                              margin='none',
                                              align='end',
                                              gravity='top'
                                          ),
                                      ],
                                      flex=1,
                                      spacing='sm',
                                      margin='md',
                                  )
                              )))


