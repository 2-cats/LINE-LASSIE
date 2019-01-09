
from flask import Flask
from flask_mqtt import Mqtt
from linebot.models import TextSendMessage


def make_report(mqtt, line_user_id):
    mqtt.publish('mytopic', 'any message you want to pubish')
    return TextSendMessage(text='好的，我正在為您準備報表，請稍候！')
