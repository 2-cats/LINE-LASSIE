import json
import unittest

import responses
from linebot import LineBotApi

from app.chatbot.device import have_device_message, no_device_message


class NoDeviceTestCase(unittest.TestCase):
    def setUp(self):
        '''
        Set up test
        '''
        # test data
        self.result_message = no_device_message()
        self.expected_message = {
            'text': '您尚未使用任何萊西！',
            'type': 'text'
        }

    def test_no_device_message(self):
        self.assertEqual(
            (json.loads(str(self.result_message))),
            self.expected_message
        )

class HaveDeviceTestCase(unittest.TestCase):
    def setUp(self):
        '''
        Set up test
        '''
        # test data
        self.devices_data = [
            {
                "name": "test_01",
                "device_status": "離線",
                "text_color": "#FF3333"
            },
            {
                "name": "test_02",
                "device_status": "連接中",
                "text_color": "#1DB446"
            }
        ]

        self.result_message = have_device_message(self.devices_data)
        self.expected_message = {
            "altText": "您的設備清單",
            "contents": {
                "contents": [
                {
                    "body": {
                    "contents": [
                        {
                        "size": "lg",
                        "text": "test_01",
                        "type": "text",
                        "weight": "bold",
                        "wrap": True
                        },
                        {
                        "color": "#FF3333",
                        "margin": "md",
                        "size": "sm",
                        "text": "離線",
                        "type": "text",
                        "wrap": True
                        }
                    ],
                    "layout": "vertical",
                    "type": "box"
                    },
                    "type": "bubble"
                },
                {
                    "body": {
                    "contents": [
                        {
                        "size": "lg",
                        "text": "test_02",
                        "type": "text",
                        "weight": "bold",
                        "wrap": True
                        },
                        {
                        "color": "#1DB446",
                        "margin": "md",
                        "size": "sm",
                        "text": "連接中",
                        "type": "text",
                        "wrap": True
                        }
                    ],
                    "layout": "vertical",
                    "type": "box"
                    },
                    "type": "bubble"
                }
                ],
                "type": "carousel"
            },
            "type": "flex"
            }

    def test_have_device_message(self):
        self.assertEqual(
            (json.loads(str(self.result_message))),
            self.expected_message
        )
