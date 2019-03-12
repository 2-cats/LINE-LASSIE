import json
import unittest

from app import create_app, db
from app.chatbot.follow import follow_message, unfollow
from app.models import User


class FollowTestCase(unittest.TestCase):
    '''
    Test follow
    '''
    def setUp(self):
        '''
        Set up test
        '''
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create fake User data
        user = User(
            line_user_id='line_user_id',
            aws_user_name='aws_user_name'
        )

        db.session.add_all([user])
        db.session.commit()

        # test data
        self.expected_message = {
            "type":"flex",
            "altText":"歡迎您的加入",
            "contents":{
                "type":"bubble",
                "body":{
                    "contents":[
                        {
                            "size":"lg",
                            "text":"歡迎加入",
                            "type":"text",
                            "weight":"bold",
                            "wrap":True
                        },
                        {
                            "margin":"md",
                            "size":"md",
                            "text":"您好，我是 Lassie！我致力於打造一個連結各種設備與用戶之間聰明、可靠、友善的互動系統，讓用戶能隨時掌握設備狀況建立連結！第一次使用請先完成綁定喔！",
                            "type":"text",
                            "wrap":True
                        }
                    ],
                    "layout":"vertical",
                    "type":"box"
                }
            }
        }

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_follow_message(self):
        '''
        Test reply follow event message
        '''
        self.assertEqual(
            (json.loads(str(follow_message()))),
            self.expected_message
        )

    def test_unfollow(self):
        unfollow('line_user_id')
        user = User.query.filter_by(
            line_user_id='line_user_id',
            deleted_at=None
        ).first()
        self.assertEqual(
            user,
            None
        )
