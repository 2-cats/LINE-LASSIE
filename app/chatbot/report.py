from flask import Flask
from flask_mqtt import Mqtt
from linebot.models import TextSendMessage

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# MQTT
app.config['MQTT_BROKER_URL'] = app.config["MQTT_HOSTNAME"]
app.config['MQTT_BROKER_PORT'] = app.config["MQTT_PORT"]
app.config['MQTT_USERNAME'] = app.config["MQTT_USERNAME"]
app.config['MQTT_PASSWORD'] = app.config["MQTT_PASSWORD"]
mqtt = Mqtt(app)

def make_report_message(line_user_id):
    make_report(line_user_id)
    return TextSendMessage(text='好的，我正在為您準備報表，請稍候！')

def make_report(line_user_id):
    mqtt.publish('mytopic', 'any message you want to pubish')
    return 0
