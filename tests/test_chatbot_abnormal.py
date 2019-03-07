import json
import unittest

import responses
from linebot import LineBotApi

from app.chatbot.abnormal import no_device_message_for_alarmlist


class NoDeviceTestCase(unittest.TestCase):
    def setUp(self):
        '''
        Set up test
        '''
        # test data
        self.result_message = no_device_message_for_alarmlist()
        self.expected_message = {
            'text': '搜尋不到任何萊西！',
            'type': 'text'
        }

    def test_no_device_message(self):
        self.assertEqual(
            (json.loads(str(self.result_message))),
            self.expected_message
        )
