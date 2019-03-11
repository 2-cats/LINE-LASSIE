from flask import Flask, abort, current_app, render_template, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (AudioMessage, FollowEvent, ImageMessage,
                            LocationMessage, MessageEvent, StickerMessage,
                            TextMessage, TextSendMessage, UnfollowEvent)

from . import liff
from .. import db
from .bind import bind_user

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
line_bot_api = LineBotApi(app.config["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(app.config["LINE_CHANNEL_SECRET"])


@liff.route("/line/bind_email", methods=['GET'])
def line_bind_email_view():
    return render_template('line/bind/email.html')

@liff.route("/line/bind_phone", methods=['POST'])
def line_bind_phone_view():
    email = request.values['email']
    return render_template(
        'line/bind/phone.html',
        email=email
    )

@liff.route("/line/bind_check", methods=['POST'])
def line_bind_view():
    email = request.values['email']
    phone = request.values['phone']
    line_user_id = request.values['line_user_id']
    messages = bind_user(email, phone, line_user_id)
    return render_template(
        'line/bind/check.html',
        messages=messages
    )

@liff.route("/line/daily_report", methods=['GET'])
def line_daily_report():
    data=request.args.get('data')
    return render_template(
        'line/report/daily.html',
        davice_data=data
    )
