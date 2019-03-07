import datetime
import unittest

from flask import Flask

from app import create_app, db
from app.liff.bind import (bind_line_user_id, bind_user,
                           check_line_user_id_exist, check_username_exist,
                           query_user_data)
from app.models import User
from config import config

app = Flask(__name__)
app.config.from_object(config['testing'])

class BindTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create fake User data
        user = User(
            line_user_id='line_user_id',
            aws_user_name='aws_user_name'
        )

        self.bind_email = "smart032410@gmail.com"
        self.unbind_email = "unknow@goodlinker.io"

        db.session.add_all([user])
        db.session.commit()

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()
    
    def test_check_username_exist(self):
        self.assertEquals(check_username_exist('aws_user_name'), True)
        self.assertEquals(check_username_exist('x'), False)
        return 0

    def test_check_line_user_id_exist(self):
        self.assertEquals(check_line_user_id_exist('line_user_id'), True)
        self.assertEquals(check_line_user_id_exist('x'), False)
        return 0

    def test_query_user_data(self):
        # If LINE user is exist.
        self.assertEquals(
            query_user_data(
                'email',
                'phone_number',
                'line_user_id'
            ),
            ['LINE 帳號已經被綁定過']
        )
        self.assertEquals(
            query_user_data(
                'email',
                'bind_phone',
                'x'
            ),
            ['找不到使用者']
        )
        return 0

    def test_bind_user(self):
        # If LINE user is exist.
        self.assertEquals(
            bind_user(
                'email',
                'phone_number',
                'line_user_id'
            ),
            ['LINE 帳號已經被綁定過']
        )
        self.assertEquals(
            bind_user(
                'email',
                'bind_phone',
                'x'
            ),
            ['找不到使用者']
        )
        return 0
