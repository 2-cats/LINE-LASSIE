from flask import Flask, abort, current_app, render_template, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (AudioMessage, FollowEvent, ImageMessage,
                            LocationMessage, MessageEvent, StickerMessage,
                            TextMessage, TextSendMessage, UnfollowEvent)

from . import liff
from .. import db
from .bind import bind_user
from .rds import connect
from .richmenu import unlink_rm

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(app.config["LINE_CHANNEL_SECRET"])


@liff.route("/line/bind_email", methods=['GET'])
def line_bind_email_view():
    return render_template('line/bind_email.html')

@liff.route("/line/bind_phone", methods=['POST'])
def line_bind_phone_view():
    email = request.values['email']
    return render_template('line/bind_phone.html', email = email)

@liff.route("/line/bind_check", methods=['POST'])
def line_bind_view():
    email = request.values['email']
    phone = request.values['phone']
    line_user_id = request.values['line_user_id']
    check_result = bind_user(email, phone, line_user_id)
    return render_template('line/bind_check.html', check_result = check_result)
