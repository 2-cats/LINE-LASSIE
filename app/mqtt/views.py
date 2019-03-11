import json

from flask import Flask, Response, request
from flask_mqtt import Mqtt
from linebot import LineBotApi

from . import mqtt
from .. import db
from .alarm import lassie_alarm_message
from .report import lassie_report_message, make_report
from .user import get_push_id, username_to_line_user_id

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# LINE ACCESS
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])


