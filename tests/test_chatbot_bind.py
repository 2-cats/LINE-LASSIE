import datetime
import unittest

from flask import Flask

from app import create_app, db
from app.chatbot.bind import check_bind
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

    def test_check_bind(self):
        self.assertEquals(check_bind('line_user_id'), True)
        self.assertEquals(check_bind('x'), False)
        return 0
