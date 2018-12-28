import json
import time

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


def lassie_alarm_message(mqtt_message):

    push_id = username_to_line_user_id(mqtt_message['u'])

    if mqtt_message['t'] == "counter":
        thing_mqtt_message=(''.join(["您" , str(mqtt_message['nt']) , "的" , str(mqtt_message['ns']) , "於" , str(
            mqtt_message['time']) , "出現異常" , "   " , "規則為" , ":" , str(mqtt_message['r']) , "異常值" , ":" , str(mqtt_message['v'])]))
        line_bot_api.push_message(push_id, TextSendMessage(text=thing_mqtt_message))  # 前提是要吃JSON訊息 才會有取ELEMEMT
    if mqtt_message['t'] == "lamp":
        thing_mqtt_message=(''.join(["您" , str(mqtt_message['nt']) , "的" , str(mqtt_message['ns']) , "於" , str(
            mqtt_message['time']) , "出現異常" , "   " , "規則為" , ":" , str(mqtt_message['r']) , "異常值" , ":" , str(mqtt_message['v'])]))
        line_bot_api.push_message(push_id, TextSendMessage(text=thing_mqtt_message))  # 前提是要吃JSON訊息 才會有取ELEMEMT
    if mqtt_message['t'] == "current":
        thing_mqtt_message=(''.join(["您" , str(mqtt_message['nt']) , "的" , str(mqtt_message['ns']) , "於" , str(
            mqtt_message['time']) , "出現異常" , "   " , "規則為" , ":" , str(mqtt_message['r']) , "異常值" , ":" , str(mqtt_message['v'])]))
        line_bot_api.push_message(push_id, TextSendMessage(text=thing_mqtt_message))  # 前提是要吃JSON訊息 才會有取ELEMEMT
    if mqtt_message['t'] == "state":
        thing_mqtt_message=(''.join(["您" , str(mqtt_message['nt']) , "的" , str(mqtt_message['ns']) , "於" , str(
            mqtt_message['time']) , "出現異常" , "   " , "規則為" , ":" , str(mqtt_message['r']) , "異常值" , ":" , str(mqtt_message['v'])]))
        line_bot_api.push_message(push_id, TextSendMessage(text=thing_mqtt_message))  # 前提是要吃JSON訊息 才會有取ELEMEMT
    if mqtt_message['t'] == "temperature":
        thing_mqtt_message=(''.join(["您" , str(mqtt_message['nt']) , "的" , str(mqtt_message['ns']) , "於" , str(
            mqtt_message['time']) , "出現異常" , "   " , "上下限為" , ":" , str(mqtt_message['ra']['h']) , "及" , str(
            mqtt_message['ra']['l']) , "   " , "異常值" , ":" , str(mqtt_message['v'])]))
        line_bot_api.push_message(push_id, TextSendMessage(text=thing_mqtt_message))  # 前提是要吃JSON訊息 才會有取ELEMEMT
    if mqtt_message['t'] == "humidity":
        thing_mqtt_message=(''.join(["您" , str(mqtt_message['nt']) , "的" , str(mqtt_message['ns']) , "於" , str(
            mqtt_message['time']) , "出現異常" , "   " , "上下限為" , ":" , str(mqtt_message['ra']['h']) , "及" , str(
            mqtt_message['ra']['l']) , "   " , "異常值" , ":" , str(mqtt_message['v'])]))
        line_bot_api.push_message(push_id, TextSendMessage(text=thing_mqtt_message))  # 前提是要吃JSON訊息 才會有取ELEMEMT
    if mqtt_message['t'] == "color":
        thing_mqtt_message=(''.join(["您" , str(mqtt_message['nt']) , "的" , str(mqtt_message['ns']) , "於" , str(
            mqtt_message['time']) , "出現異常" , "   " , "規則為" , ":" , str(mqtt_message['r']) , "異常值" , ":" , str(mqtt_message['v'])]))
        line_bot_api.push_message(push_id, TextSendMessage(text=thing_mqtt_message))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        line_bot_api.push_message(push_id, ImageSendMessage(original_content_url=str(mqtt_message['url']),
                                                                    preview_image_url=str(mqtt_message['url'])))
    if mqtt_message['t'] == "detector":
        thing_mqtt_message=(''.join(["您" , str(mqtt_message['nt']) , "的" , str(mqtt_message['ns']) , "於" , str(
            mqtt_message['time']) , "出現異常" , "   " , "規則為" , ":" , str(mqtt_message['r']) , "異常值" , ":" , str(mqtt_message['v'])]))
        line_bot_api.push_message(push_id, TextSendMessage(text=thing_mqtt_message))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        line_bot_api.push_message(push_id, ImageSendMessage(original_content_url=str(mqtt_message['url']),
                                                                    preview_image_url=str(mqtt_message['url'])))
    if mqtt_message['t'] == "timer":
        thing_mqtt_message=(''.join(["您" , str(mqtt_message['nt']) , "的" , str(mqtt_message['ns']) , "於" , str(
            mqtt_message['time']) , "出現異常" , "   " , "規則為" , ":" , str(mqtt_message['r']) , "異常值" , ":" , str(mqtt_message['v'])]))
        line_bot_api.push_message(push_id, TextSendMessage(text=thing_mqtt_message))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        line_bot_api.push_message(push_id, ImageSendMessage(original_content_url=str(mqtt_message['url']),
                                                                    preview_image_url=str(mqtt_message['url'])))
    if mqtt_message['t'] == "ocr":
        thing_mqtt_message=(''.join(["您" , str(mqtt_message['nt']) , "的" , str(mqtt_message['ns']) , "於" , str(
            mqtt_message['time']) , "出現異常" , "   " , "上下限為" , ":" , str(mqtt_message['ra']['h']) , "及" , str(
            mqtt_message['ra']['l']) , "   " , "異常值" , ":" , str(mqtt_message['v'])]))
        line_bot_api.push_message(push_id, TextSendMessage(text=thing_mqtt_message))  # 前提是要吃JSON訊息 才會有取ELEMEMT
        line_bot_api.push_message(push_id, ImageSendMessage(original_content_url=str(mqtt_message['url']),
                                                                    preview_image_url=str(mqtt_message['url'])))
