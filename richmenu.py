from flask import Flask
from linebot import LineBotApi

import config

app = Flask(__name__)

# Get app config
app.config.from_object(config)

line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])

def unlink_rm(line_user_id):
    line_bot_api.unlink_rich_menu_from_user(line_user_id)

def link_rm_to_user(line_user_id):
    '''
    Link rich menu to user
    '''
    line_bot_api.link_rich_menu_to_user(line_user_id, app.config['USER_RICH_MENU_ID'])
