import json
import unittest

from app import create_app, db
from app.chatbot.bind import bind_member, check_bind, check_room_and_group_bind
from app.models import Member, User


class CheckBindTestCase(unittest.TestCase):
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

        member1 = Member(
            source_id='line_room_id',
            source_type='room',
            user_id=user.id,
        )

        member2 = Member(
            source_id='line_group_id',
            source_type='group',
            user_id=user.id,
        )

        self.bind_email = "smart032410@gmail.com"
        self.unbind_email = "unknow@goodlinker.io"

        db.session.add_all([user, member1, member2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_check_bind(self):
        self.assertEquals(check_bind('line_user_id'), True)
        self.assertEquals(check_bind('x'), False)
        return 0
    
    def test_check_room_and_group_bind(self):
        self.assertEquals(check_room_and_group_bind('line_room_id', 'room'), True)
        self.assertEquals(check_room_and_group_bind('line_group_id', 'group'), True)
        self.assertEquals(check_room_and_group_bind('x', 'x'), False)

class BindTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        user = User(
            line_user_id='line_user_id',
            aws_user_name='aws_user_name'
        )

        db.session.add_all([user])
        db.session.commit()

        self.bind_new_room_result_message = bind_member('line_user_id', 'line_room_id', 'room')
        self.bind_new_room_expected_message = {
            'text': '綁定成功',
            'type': 'text'
        }

        self.bind_new_group_result_message = bind_member('line_user_id', 'line_group_id', 'group')
        self.bind_new_group_expected_message = {
            'text': '綁定成功',
            'type': 'text'
        }

        self.bind_old_room_result_message = bind_member('line_user_id', 'line_room_id', 'room')
        self.bind_old_room_expected_message = {
            'text': '綁定失敗',
            'type': 'text'
        }

        self.bind_old_group_result_message = bind_member('line_user_id', 'line_group_id', 'group')
        self.bind_old_group_expected_message = {
            'text': '綁定失敗',
            'type': 'text'
        }

    def tearDown(self):
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_bind_member(self):
        self.assertEquals(
            json.loads(str(self.bind_new_room_result_message)),
            self.bind_new_room_expected_message
        )
        self.assertEquals(
            json.loads(str(self.bind_new_group_result_message)),
            self.bind_new_group_expected_message
        )
        self.assertEquals(
            json.loads(str(self.bind_old_room_result_message)),
            self.bind_old_room_expected_message
        )
        self.assertEquals(
            json.loads(str(self.bind_old_group_result_message)),
            self.bind_old_group_expected_message
        )
