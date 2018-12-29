from datetime import datetime

from flask import Flask
from flask_login import AnonymousUserMixin, UserMixin
from linebot import LineBotApi
from werkzeug.security import check_password_hash, generate_password_hash

import config

from . import db

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    line_user_id = db.Column(db.String(64), unique=True)
    aws_user_name = db.Column(db.String(64), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<User %r>' % self.line_user_id

    def link_rm_to_guest(self):
        '''
        Link rich menu to guest
        '''
        line_bot_api.link_rich_menu_to_user(self.line_user_id, app.config['GUEST_RICH_MENU_ID'])

    def link_rm_to_user(self):
        '''
        Link rich menu to user
        '''
        line_bot_api.link_rich_menu_to_user(self.line_user_id, app.config['USER_RICH_MENU_ID'])
