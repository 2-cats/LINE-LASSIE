from flask import Flask
from flask_mqtt import Mqtt
from linebot.models import TextSendMessage

from ..models import User

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
    message = TextSendMessage(
        text='好的，我正在為您準備報表，請稍候！'
    )
    return message

def make_report(line_user_id):
    user = User.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()
    topic = ''.join(
        [
            '/lassie/',
            user.aws_user_name,
            '/getTodayReport'
        ]
    )
    mqtt.publish(topic, None)
    return 0
