import json
import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from flask import Flask
from linebot import LineBotApi, WebhookHandler
from linebot.models import (BoxComponent, BubbleContainer, FlexSendMessage,
                            ImageComponent, ImageSendMessage, MessageAction,
                            MessageEvent, TextComponent, TextSendMessage)
from .user import username_to_line_user_id
import config


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

#MQTT
HOST = app.config['MQTT_HOSTNAME']
PORT = app.config['MQTT_PORT']

line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])
# Channel Secret
handler = WebhookHandler(app.config['LINE_CHANNEL_SECRET'])


def client_loop():
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    client = mqtt.Client(client_id)    #client_id不能重复，所以使用当前时间
    client.username_pw_set(app.config['MQTT_USERNAME'], app.config['MQTT_PASSWORD'])  #必须设置，否则会返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 60)
    client.loop_forever()
    
def on_connect(client, userdata, flags, rc):
    client.subscribe("/line/gl1/lassie/alarm")
    client.subscribe("/line/gl1/lassie/alarmlist")
    
def on_message(client, userdata, msg):
    json_data=json.loads(msg.payload.decode("utf-8"))
    if msg.topic == "/line/gl1/lassie/alarm":
        push_id=username_to_line_user_id(json_data['u'])

        if json_data['t'] == "counter":
            thing_msg=(''.join(["您" , str(json_data['nt']) , "的" , str(json_data['ns']) , "於" , str(
                json_data['time']) , "出現異常" , "   " , "規則為" , ":" , str(json_data['r']) , "異常值" , ":" , str(json_data['v'])]))
            line_bot_api.push_message(push_id, TextSendMessage(text=thing_msg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        if json_data['t'] == "lamp":
            thing_msg=(''.join(["您" , str(json_data['nt']) , "的" , str(json_data['ns']) , "於" , str(
                json_data['time']) , "出現異常" , "   " , "規則為" , ":" , str(json_data['r']) , "異常值" , ":" , str(json_data['v'])]))
            line_bot_api.push_message(push_id, TextSendMessage(text=thing_msg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        if json_data['t'] == "current":
            thing_msg=(''.join(["您" , str(json_data['nt']) , "的" , str(json_data['ns']) , "於" , str(
                json_data['time']) , "出現異常" , "   " , "規則為" , ":" , str(json_data['r']) , "異常值" , ":" , str(json_data['v'])]))
            line_bot_api.push_message(push_id, TextSendMessage(text=thing_msg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        if json_data['t'] == "state":
            thing_msg=(''.join(["您" , str(json_data['nt']) , "的" , str(json_data['ns']) , "於" , str(
                json_data['time']) , "出現異常" , "   " , "規則為" , ":" , str(json_data['r']) , "異常值" , ":" , str(json_data['v'])]))
            line_bot_api.push_message(push_id, TextSendMessage(text=thing_msg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        if json_data['t'] == "temperature":
            thing_msg=(''.join(["您" , str(json_data['nt']) , "的" , str(json_data['ns']) , "於" , str(
                json_data['time']) , "出現異常" , "   " , "上下限為" , ":" , str(json_data['ra']['h']) , "及" , str(
                json_data['ra']['l']) , "   " , "異常值" , ":" , str(json_data['v'])]))
            line_bot_api.push_message(push_id, TextSendMessage(text=thing_msg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        if json_data['t'] == "humidity":
            thing_msg=(''.join(["您" , str(json_data['nt']) , "的" , str(json_data['ns']) , "於" , str(
                json_data['time']) , "出現異常" , "   " , "上下限為" , ":" , str(json_data['ra']['h']) , "及" , str(
                json_data['ra']['l']) , "   " , "異常值" , ":" , str(json_data['v'])]))
            line_bot_api.push_message(push_id, TextSendMessage(text=thing_msg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        if json_data['t'] == "color":
            thing_msg=(''.join(["您" , str(json_data['nt']) , "的" , str(json_data['ns']) , "於" , str(
                json_data['time']) , "出現異常" , "   " , "規則為" , ":" , str(json_data['r']) , "異常值" , ":" , str(json_data['v'])]))
            line_bot_api.push_message(push_id, TextSendMessage(text=thing_msg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
            line_bot_api.push_message(push_id, ImageSendMessage(original_content_url=str(json_data['url']),
                                                                     preview_image_url=str(json_data['url'])))
        if json_data['t'] == "detector":
            thing_msg=(''.join(["您" , str(json_data['nt']) , "的" , str(json_data['ns']) , "於" , str(
                json_data['time']) , "出現異常" , "   " , "規則為" , ":" , str(json_data['r']) , "異常值" , ":" , str(json_data['v'])]))
            line_bot_api.push_message(push_id, TextSendMessage(text=thing_msg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
            line_bot_api.push_message(push_id, ImageSendMessage(original_content_url=str(json_data['url']),
                                                                     preview_image_url=str(json_data['url'])))
        if json_data['t'] == "timer":
            thing_msg=(''.join(["您" , str(json_data['nt']) , "的" , str(json_data['ns']) , "於" , str(
                json_data['time']) , "出現異常" , "   " , "規則為" , ":" , str(json_data['r']) , "異常值" , ":" , str(json_data['v'])]))
            line_bot_api.push_message(push_id, TextSendMessage(text=thing_msg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
            line_bot_api.push_message(push_id, ImageSendMessage(original_content_url=str(json_data['url']),
                                                                     preview_image_url=str(json_data['url'])))
        if json_data['t'] == "ocr":
            thing_msg=(''.join(["您" , str(json_data['nt']) , "的" , str(json_data['ns']) , "於" , str(
                json_data['time']) , "出現異常" , "   " , "上下限為" , ":" , str(json_data['ra']['h']) , "及" , str(
                json_data['ra']['l']) , "   " , "異常值" , ":" , str(json_data['v'])]))
            line_bot_api.push_message(push_id, TextSendMessage(text=thing_msg))  # 前提是要吃JSON訊息 才會有取ELEMEMT
            line_bot_api.push_message(push_id, ImageSendMessage(original_content_url=str(json_data['url']),
                                                                     preview_image_url=str(json_data['url'])))
