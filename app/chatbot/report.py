import requests
from flask import Flask
from flask_mqtt import Mqtt
from linebot.models import TextSendMessage

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')


def make_report_message(line_user_id):
    payload = {'line_user_id': line_user_id}

    url = ''.join(
        [
            app.config['APP_URL'],
            'mqtt/report/send/today'
        ]
    )
    requests.get(url, params=payload)
    message = TextSendMessage(
        text='好的，我正在為您準備報表，請稍候！'
    )
    return message
