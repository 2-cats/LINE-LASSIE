import json

from flask import Flask
from flask_mqtt import Mqtt
from linebot import LineBotApi

from . import mqtt
from .. import db
from .alarm import lassie_alarm_message
from .report import lassie_report
from .user import username_to_line_user_id

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# LINE ACCESS
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])

# MQTT
app.config['MQTT_BROKER_URL'] = app.config["MQTT_HOSTNAME"]
app.config['MQTT_BROKER_PORT'] = app.config["MQTT_PORT"]
app.config['MQTT_USERNAME'] = app.config["MQTT_USERNAME"]
app.config['MQTT_PASSWORD'] = app.config["MQTT_PASSWORD"]
mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe("/line/gl1/lassie/alarm")
    mqtt.subscribe("/line/gl1/lassie/report")


# Handle MQTT message
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    if topic == "/line/gl1/lassie/alarm":
        payload = json.loads(message.payload.decode())
        message = lassie_alarm_message(payload)
        line_user_id = username_to_line_user_id(payload['u'])
        line_bot_api.push_message(line_user_id, message)
        return 0
    elif topic == "/line/gl1/lassie/report":
        payload = json.loads(message.payload.decode())
        message = lassie_report(payload)
        line_user_id = username_to_line_user_id(payload['u'])
        line_bot_api.push_message(line_user_id, message)
        return 0
