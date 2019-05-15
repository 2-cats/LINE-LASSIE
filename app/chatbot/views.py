import json

from flask import Flask, abort, current_app, render_template, request
from flask_mqtt import Mqtt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (AudioMessage, FollowEvent, ImageMessage, JoinEvent,
                            LocationMessage, MessageEvent, PostbackEvent,
                            StickerMessage, TextMessage, TextSendMessage,
                            UnfollowEvent)

from .. import db, mqtt
from . import chatbot
from .abnormal import alarm_list_message, abnormal_pic_message, summary
from .alarm import lassie_alarm_message
from .bind import bind_member, check_bind
from .contact import contact_us
from .device import device_list_message
from .error_message import alert_no_action_message, alert_to_bind_message
from .follow import follow_message, unfollow
from .report import lassie_report_message, make_report_message
from .target import get_push_id, username_to_line_user_id

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# LINE ACCESS
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(app.config["LINE_CHANNEL_SECRET"])


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
    message = follow_message()
    line_bot_api.reply_message(event.reply_token, message)
    return 0

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    '''
    Handle unfollow event
    '''
    unfollow(event.source.user_id)
    return 0

# Handle MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # Get common LINE user information
    line_user_id = event.source.user_id
    message_text = event.message.text
    source_type = event.source.type

    if source_type == 'user':
        if message_text == "get_me_line_user_id":
            message = TextSendMessage(text=str(line_user_id))
            line_bot_api.reply_message(event.reply_token, message)
            return 0

        # Check user is bind
        if check_bind(line_user_id):
            if message_text == "異常總覽":
                message = TextSendMessage(text='稍等一下！我正在搜尋您的萊西...')
                line_bot_api.reply_message(event.reply_token, message)
                message = alarm_list_message(line_user_id)
                line_bot_api.push_message(line_user_id, message)
                return 0
            if message_text == "聯絡我們":
                message = contact_us(line_user_id)
                line_bot_api.reply_message(event.reply_token, message)
                return 0
            if message_text == "設備清單":
                message = TextSendMessage(text='稍等一下！我正在找您的萊西...')
                line_bot_api.reply_message(event.reply_token, message)
                message = device_list_message(line_user_id)
                line_bot_api.push_message(line_user_id, message)
                return 0
            if message_text == "今日報表":
                message = make_report_message(mqtt, line_user_id)
                line_bot_api.reply_message(event.reply_token, message)
                return 0
            message = alert_no_action_message()
            line_bot_api.reply_message(event.reply_token, message)
            return 0
        message = alert_to_bind_message()
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    elif source_type == 'room':
        if message_text == "綁定萊西":
            message = bind_member(line_user_id, event.source.room_id, 'room')
            line_bot_api.reply_message(event.reply_token, message)
            return 0
    elif source_type == 'group':
        if message_text == "綁定萊西":
            message = bind_member(line_user_id, event.source.group_id, 'group')
            line_bot_api.reply_message(event.reply_token, message)
            return 0

# Postback Event
@handler.add(PostbackEvent)
def handle_postback(event):
    line_user_id = event.source.user_id
    # data="action, var1, var2, ... ,varN"
    # Convet to postback_data: [action, var1, var2, ... ,varN]
    postback_data = event.postback.data.split(",")
    if postback_data[0] == "abnormal":
        thing_id = postback_data[1]
        message = summary(thing_id)
        line_bot_api.reply_message(event.reply_token, message)
        return 0

    if postback_data[0] == "get_abnormal_pic":
        surv_url = postback_data[1]
        message = abnormal_pic_message(surv_url)
        line_bot_api.reply_message(event.reply_token, message)
        return 0

# Handle location message event
@handler.add(MessageEvent, message=LocationMessage)
def handle_loaction_message(event):
    """"
    Handle location message Event.
    """
    line_user_id = event.source.user_id
    source_type = event.source.type
    if source_type == 'user':
        message = alert_no_action_message()
        line_bot_api.reply_message(event.reply_token, message)
        return 0

# Handle image message event
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    source_type = event.source.type
    if source_type == 'user':
        line_user_id = event.source.user_id
        message = alert_no_action_message()
        line_bot_api.reply_message(event.reply_token, message)
        return 0

# Handle audio message event
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    source_type = event.source.type
    if source_type == 'user':
        line_user_id = event.source.user_id
        message = alert_no_action_message()
        line_bot_api.reply_message(event.reply_token, message)
        return 0

# Handle sticker message event
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    source_type = event.source.type
    if source_type == 'user':
        line_user_id = event.source.user_id
        message = alert_no_action_message()
        line_bot_api.reply_message(event.reply_token, message)
        return 0



@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe("@goodlinker/notification/rule")
    mqtt.subscribe("/lassie/getTodayReport")


# Handle MQTT message
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    if topic == '@goodlinker/notification/rule':
        payload = json.loads(message.payload.decode())
        message = lassie_alarm_message(payload)
        line_user_id = get_push_id(payload['endUserSub'])
        line_bot_api.push_message(line_user_id, message)
        return 0
    elif topic == '/lassie/getTodayReport':
        payload = json.loads(message.payload.decode())
        message = lassie_report_message(payload)
        line_user_id = username_to_line_user_id(payload['u'])
        line_bot_api.push_message(line_user_id, message)
        return 0
