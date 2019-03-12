import json
import unittest

from app import create_app, db, mqtt
from app.chatbot.report import make_report_message
from app.models import User


class ReportTestCase(unittest.TestCase):
    '''
    Test report
    '''
    def setUp(self):
        '''
        Set up test
        '''
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

        # test data
        self.result_message = make_report_message(mqtt, "line_user_id")
        self.expected_message = {
            'text': '好的，我正在為你準備報表，請稍候',
            'type': 'text'
        }
    
    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_report_message(self):
        '''
        Test reply report message
        '''
        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )
