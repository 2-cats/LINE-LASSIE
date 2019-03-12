import json
import unittest

from app.chatbot.report import make_report_message
from app import mqtt

class ReportTestCase(unittest.TestCase):
    '''
    Test report
    '''
    def setUp(self):
        '''
        Set up test
        '''
        # test data
        self.result_message = make_report_message(mqtt, "line_user_id")
        self.expected_message = {
            'text': '好的，我正在為你準備報表，請稍候',
            'type': 'text'
        }

    def test_report_message(self):
        '''
        Test reply report message
        '''
        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )
