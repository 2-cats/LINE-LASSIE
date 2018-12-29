from flask import Flask
from linebot import LineBotApi

import config

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])

def link_rm_to_guest(line_user_id):
    '''
    Link rich menu to guest
    '''
    line_bot_api.link_rich_menu_to_user(line_user_id, app.config['GUEST_RICH_MENU_ID'])
