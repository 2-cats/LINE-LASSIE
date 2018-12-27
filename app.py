import threading

from flask import Flask, abort, render_template, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage

import config
from abnormal import summary
from bind import bind_line_message, bind_user, check_bind
from mqtt import client_loop

app = Flask(__name__)

# Get app config
app.config.from_object(config)

# Channel Access Token
line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])
# Channel Secret
handler = WebhookHandler(app.config['LINE_CHANNEL_SECRET'])

# LIFF
@app.route("/line/bind_email", methods=['GET'])
def line_bind_email_view():
    return render_template('line/bind_email.html')

@app.route("/line/bind_phone", methods=['POST'])
def line_bind_phone_view():
    email = request.values['email']
    return render_template('line/bind_phone.html', email = email)

@app.route("/line/bind_check", methods=['POST'])
def line_bind_view():
    email = request.values['email']
    phone = request.values['phone']
    line_user_id = request.values['line_user_id']
    check_result = bind_user(email, phone, line_user_id)
    return render_template('line/bind_check.html', check_result = check_result)

@app.route("/callback", methods=['POST'])
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

# Handle MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # Get common LINE user information
    line_user_id = event.source.user_id
    message_text = event.message.text

    # Check user is bind
    if check_bind(line_user_id):
        if message_text == "異常總表":
            message = summary(line_user_id)
            line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    threading.Thread(target=client_loop).start()
    app.run()
