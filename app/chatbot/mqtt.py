import pymysql
from flask import Flask
from linebot import LineBotApi, WebhookHandler
from linebot.models import (BoxComponent, BubbleContainer, FlexSendMessage,
                            ImageComponent, ImageSendMessage, TextComponent,IconComponent)

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(app.config["LINE_CHANNEL_SECRET"])

def lassie_alarm_message(mqtt_message):
    push_id = username_to_line_user_id(mqtt_message['u'])
    unit = ''
    if mqtt_message['t'] == 'counter':
        unit = ' (次)'
    if mqtt_message['t'] == 'lamp' or 'state' or 'color' or 'detector' or 'ocr':
        unit = ' (偵測值)'
    if mqtt_message['t'] == 'current':
        unit = ' (mAh)'
    if mqtt_message['t'] == 'temperature':
        unit = ' (℃)'
    if mqtt_message['t'] == 'humidity':
        unit = ' (%)'
    if mqtt_message['t'] == 'timer':
        unit = ' (秒)'
    message_list = []
    message = ImageSendMessage(
                                original_content_url=str(mqtt_message['url']),
                                preview_image_url=str(mqtt_message['url'])
                              )
    message_list.append(message)
    message = FlexSendMessage(
                              alt_text='異常通知',
                              contents=BubbleContainer(
                                  hero=ImageComponent(
                                      url='https://i.imgur.com/EzEglZZ.png',
                                      size='full',
                                      aspect_ratio='2:1',
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
                                                          IconComponent(
                                                              aspect_ratio='1:1',
                                                              margin='none',
                                                              size='md',
                                                              url='https://i.imgur.com/OoRVQey.png'
                                                          ),
                                                          TextComponent(
                                                              text=mqtt_message['ns'],
                                                              weight='bold',
                                                              wrap=False,
                                                              size='md',
                                                              color='#464646',
                                                              flex=0,
                                                              margin='sm',
                                                              align='start',
                                                              gravity='top'
                                                          ),
                                                          TextComponent(
                                                              text=str(mqtt_message['v']) + unit,
                                                              weight='regular',
                                                              wrap=False,
                                                              size='sm',
                                                              color='#000000',
                                                              flex=1,
                                                              margin='none',
                                                              align='end',
                                                              gravity='top'
                                                          ),
                                                      ]
                                                  )
                                              ]
                                          ),
                                          TextComponent(
                                              text=mqtt_message['time'],
                                              weight='regular',
                                              wrap=True,
                                              size='xs',
                                              color='#aaaaaa',
                                              flex=1,
                                              margin='none',
                                              align='end',
                                              gravity='top'
                                          ),
                                      ]
                                  )
                              )
                          )
    message_list.append(message)
    line_bot_api.push_message(push_id, message_list)



def username_to_line_user_id(username):
    # Convert username to line_user_id
    database = pymysql.connect(
        app.config['DB_HOST'],
        app.config['DB_USERNAME'],
        app.config['DB_PASSWORD'],
        app.config['DB_NAME'],
        charset="utf8"
    )
    cursor = database.cursor()
    args = (username,)
    cursor.execute("SELECT line_user_id FROM users WHERE aws_user_name =  %s", args)
    result = cursor.fetchone()
    database.close()
    return result[0]
