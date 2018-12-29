import json

from flask import Flask, abort, current_app, render_template, request
from flask_mqtt import Mqtt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (AudioMessage, FollowEvent, ImageMessage,
                            LocationMessage, MessageEvent, StickerMessage,
                            TextMessage, TextSendMessage, UnfollowEvent)

from . import chatbot
from .. import db
from .abnormal import summary
from .bind import check_bind
from .contact import contact_us
from .device import device_list
from .error_message import alert_no_action_message, alert_to_bind_message
from .follow import follow_message, unfollow
from .mqtt import lassie_alarm_message

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# LINE ACCESS
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(app.config["LINE_CHANNEL_SECRET"])

# MQTT
app.config['MQTT_BROKER_URL'] = app.config["MQTT_HOSTNAME"]
app.config['MQTT_BROKER_PORT'] = app.config["MQTT_PORT"]
app.config['MQTT_USERNAME'] = app.config["MQTT_USERNAME"]
app.config['MQTT_PASSWORD'] = app.config["MQTT_PASSWORD"]
mqtt = Mqtt(app)

# Subscribe MQTT: Lassie/alarm
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('/line/gl1/lassie/alarm')

# Handle MQTT message
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode()
    lassie_alarm_message(json.loads(payload))


@chatbot.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    '''
    Handle follow event
    '''
    message = follow_message(event.source.user_id)
    line_bot_api.reply_message(event.reply_token, message)
    return 0

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    '''
    Handle unfollow event
    '''
    message = unfollow(event.source.user_id)
    line_bot_api.reply_message(event.reply_token, message)
    return 0

# Handle MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # Get common LINE user information
    line_user_id = event.source.user_id
    message_text = event.message.text

    if message_text == "get_me_line_user_id":
        message = TextSendMessage(text=str(line_user_id))
        line_bot_api.reply_message(event.reply_token, message)
        return 0

    # Check user is bind
    if check_bind(line_user_id):
        if message_text == "異常總覽":
            message = summary(line_user_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        if message_text == "聯絡我們":
            message = contact_us(line_user_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        if message_text == "設備清單":
            message = device_list(line_user_id)
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        message = alert_no_action_message(line_user_id)
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    message = alert_to_bind_message(line_user_id)
    line_bot_api.reply_message(event.reply_token, message)
    return 0

# Handle location message event
@handler.add(MessageEvent, message=LocationMessage)
def handle_loaction_message(event):
    """"
    Handle location message Event.
    """
    line_user_id = event.source.user_id
    message = alert_no_action_message(line_user_id)
    line_bot_api.reply_message(event.reply_token, message)
    return 0

# Handle image message event
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    line_user_id = event.source.user_id
    message = alert_no_action_message(line_user_id)
    line_bot_api.reply_message(event.reply_token, message)
    return 0

# Handle audio message event
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    line_user_id = event.source.user_id
    message = alert_no_action_message(line_user_id)
    line_bot_api.reply_message(event.reply_token, message)
    return 0

# Handle sticker message event
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_user_id = event.source.user_id
    message = alert_no_action_message(line_user_id)
    line_bot_api.reply_message(event.reply_token, message)
    return 0
