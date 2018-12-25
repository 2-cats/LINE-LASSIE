import json
import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from linebot import LineBotApi, WebhookHandler
from linebot.models import (BoxComponent, BubbleContainer, FlexSendMessage,
                            ImageComponent, ImageSendMessage, MessageAction,
                            MessageEvent, TextComponent, TextSendMessage)

#MQTT
HOST = "m15.cloudmqtt.com"
PORT = 17407
line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])
# Channel Secret
handler = WebhookHandler(app.config['LINE_CHANNEL_SECRET'])


def client_loop():
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    client = mqtt.Client(client_id)    #client_id不能重复，所以使用当前时间
    client.username_pw_set("eycjuarq", "EluqSNPot8X2")  #必须设置，否则会返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 60)
    client.loop_forever()
    
def on_connect(client, userdata, flags, rc):
    client.subscribe("/line/gl1/lassie/alarm")
    client.subscribe("/line/gl1/lassie/alarmlist")
    
def on_message(client, userdata, msg):
    jsondata=json.loads(msg.payload.decode("utf-8"))
    if msg.topic =="/line/gl1/lassie/alarm":
        if jsondata['sensor_type'] == "count":
            countmsg=(''.join(["您" , str(jsondata['thing_name']) , "的" , str(jsondata['sensor_name']) , "於" , str(
                jsondata['time']) , "出現異常" , "   " , "規則為" , ":" , str(jsondata['rule']) , "異常值" , ":" , str(jsondata['value'])]))
            line_bot_api.push_message(jsondata['chat_id'], TextSendMessage(text=countmsg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        if jsondata['sensor_type'] == "lamp":
            countmsg=(''.join(["您" , str(jsondata['thing_name']) , "的" , str(jsondata['sensor_name']) , "於" , str(
                jsondata['time']) , "出現異常" , "   " , "規則為" , ":" , str(jsondata['rule']) , "異常值" , ":" , str(jsondata['value'])]))
            line_bot_api.push_message(jsondata['chat_id'], TextSendMessage(text=countmsg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        if jsondata['sensor_type'] == "current":
            countmsg=(''.join(["您" , str(jsondata['thing_name']) , "的" , str(jsondata['sensor_name']) , "於" , str(
                jsondata['time']) , "出現異常" , "   " , "規則為" , ":" , str(jsondata['rule']) , "異常值" , ":" , str(jsondata['value'])]))
            line_bot_api.push_message(jsondata['chat_id'], TextSendMessage(text=countmsg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        if jsondata['sensor_type'] == "state":
            countmsg=(''.join(["您" , str(jsondata['thing_name']) , "的" , str(jsondata['sensor_name']) , "於" , str(
                jsondata['time']) , "出現異常" , "   " , "規則為" , ":" , str(jsondata['rule']) , "異常值" , ":" , str(jsondata['value'])]))
            line_bot_api.push_message(jsondata['chat_id'], TextSendMessage(text=countmsg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        if jsondata['sensor_type'] == "temp":
            countmsg=(''.join(["您" , str(jsondata['thing_name']) , "的" , str(jsondata['sensor_name']) , "於" , str(
                jsondata['time']) , "出現異常" , "   " , "上下限為" , ":" , str(jsondata['ruleR']['highest']) , "及" , str(
                jsondata['ruleR']['lowest']) , "   " , "異常值" , ":" , str(jsondata['value'])]))
            line_bot_api.push_message(jsondata['chat_id'], TextSendMessage(text=countmsg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        if jsondata['sensor_type'] == "humidity":
            countmsg=(''.join(["您" , str(jsondata['thing_name']) , "的" , str(jsondata['sensor_name']) , "於" , str(
                jsondata['time']) , "出現異常" , "   " , "上下限為" , ":" , str(jsondata['ruleR']['highest']) , "及" , str(
                jsondata['ruleR']['lowest']) , "   " , "異常值" , ":" , str(jsondata['value'])]))
            line_bot_api.push_message(jsondata['chat_id'], TextSendMessage(text=countmsg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        if jsondata['sensor_type'] == "color":
            countmsg=(''.join(["您" , str(jsondata['thing_name']) , "的" , str(jsondata['sensor_name']) , "於" , str(
                jsondata['time']) , "出現異常" , "   " , "規則為" , ":" , str(jsondata['rule']) , "異常值" , ":" , str(jsondata['value'])]))
            line_bot_api.push_message(jsondata['chat_id'], TextSendMessage(text=countmsg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
            line_bot_api.push_message(jsondata['chat_id'], ImageSendMessage(original_content_url=str(jsondata['image']),
                                                                     preview_image_url=str(jsondata['image'])))
        if jsondata['sensor_type'] == "idle":
            countmsg=(''.join(["您" , str(jsondata['thing_name']) , "的" , str(jsondata['sensor_name']) , "於" , str(
                jsondata['time']) , "出現異常" , "   " , "規則為" , ":" , str(jsondata['rule']) , "異常值" , ":" , str(jsondata['value'])]))
            line_bot_api.push_message(jsondata['chat_id'], TextSendMessage(text=countmsg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
            line_bot_api.push_message(jsondata['chat_id'], ImageSendMessage(original_content_url=str(jsondata['image']),
                                                                     preview_image_url=str(jsondata['image'])))
        if jsondata['sensor_type'] == "safety":
            countmsg=(''.join(["您" , str(jsondata['thing_name']) , "的" , str(jsondata['sensor_name']) , "於" , str(
                jsondata['time']) , "出現異常" , "   " , "規則為" , ":" , str(jsondata['rule']) , "異常值" , ":" , str(jsondata['value'])]))
            line_bot_api.push_message(jsondata['chat_id'], TextSendMessage(text=countmsg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
            line_bot_api.push_message(jsondata['chat_id'], ImageSendMessage(original_content_url=str(jsondata['image']),
                                                                     preview_image_url=str(jsondata['image'])))
        if jsondata['sensor_type'] == "ocr":
            countmsg=(''.join(["您" , str(jsondata['thing_name']) , "的" , str(jsondata['sensor_name']) , "於" , str(
                jsondata['time']) , "出現異常" , "   " , "上下限為" , ":" , str(jsondata['ruleR']['highest']) , "及" , str(
                jsondata['ruleR']['lowest']) , "   " , "異常值" , ":" , str(jsondata['value'])]))
            line_bot_api.push_message(jsondata['chat_id'], TextSendMessage(text=countmsg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
            line_bot_api.push_message(jsondata['chat_id'], ImageSendMessage(original_content_url=str(jsondata['image']),
                                                                     preview_image_url=str(jsondata['image'])))
    if msg.topic == "/line/gl1/lassie/alarmlist":
        alarmlist=[]
        for i in jsondata:
            temp=TextComponent(
                text=i['sensor_type'],
                wrap=True,
                size='xl',
                color='#111111',
                margin='md'
            )
            alarmlist.append(temp)

            temp1=TextComponent(
                text=i['sensor_name'],
                wrap=True,
                weight='bold',
                size='xl',
                color='#1DB446',
                margin='md'
            )

            alarmlist.append(temp1)
        line_bot_api.push_message(i['chat_id'], TextSendMessage(text="以下是您的異常總表"))

        line_bot_api.push_message(i['chat_id'],
            FlexSendMessage(
                alt_text='異常總表',
                contents=BubbleContainer(
                    direction='ltr',
                    header=BoxComponent(
                        layout='horizontal',
                        contents=[
                            TextComponent(
                                text='異常總表',
                                wrap=True,
                                size='xxl',
                                weight='bold',
                                color='#2578d8',
                                margin='md',
                                align= "center",
                                gravity= "top",

                            ),
                        ],
                        flex=1,
                        spacing='none',
                        margin='md'
                    ),
                    hero=ImageComponent(
                        url='https://pic.pimg.tw/allaboutchenjian/1509281084-2985805543_l.jpg',
                        size='full',
                        aspect_ratio='3:1',
                        aspect_mode='cover'
                    ),
                    body=BoxComponent(
                        layout='vertical',
                        flex=1,
                        spacing='sm',
                        margin='md',
                        contents=alarmlist
                    )
                )
            )
        )
