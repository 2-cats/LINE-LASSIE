import unittest
import json

from app.chatbot.alarm import lassie_alarm_message

class AlarmCounterTestCase(unittest.TestCase):
    def setUp(self):
        self.data = {
            't' : 'counter',
            'nt': 'nt',
            'ns': 'ns',
            'v': 'v',
            'r': 'r',
            'url': '',
            'time': '2019/03/08 21:00'
        }
        self.result_message = lassie_alarm_message(self.data)
        self.expected_message = [
            {
                "altText": "異常通知",
                "contents": {
                "body": {
                    "contents": [
                    {
                        "align": "center",
                        "color": "#464646",
                        "flex": 1,
                        "gravity": "top",
                        "margin": "none",
                        "size": "xl",
                        "text": "nt 異常",
                        "type": "text",
                        "weight": "bold",
                        "wrap": True
                    },
                    {
                        "contents": [
                        {
                            "contents": [
                            {
                                "align": "start",
                                "color": "#464646",
                                "flex": 0,
                                "gravity": "top",
                                "margin": "sm",
                                "size": "md",
                                "text": "ns",
                                "type": "text",
                                "weight": "bold",
                                "wrap": True
                            },
                            {
                                "align": "end",
                                "color": "#D0021B",
                                "flex": 1,
                                "gravity": "top",
                                "margin": "md",
                                "size": "xl",
                                "text": "v (次)",
                                "type": "text",
                                "weight": "bold",
                                "wrap": False
                            }
                            ],
                            "flex": 1,
                            "layout": "baseline",
                            "margin": "md",
                            "spacing": "sm",
                            "type": "box"
                        }
                        ],
                        "flex": 1,
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "type": "box"
                    },
                    {
                        "align": "end",
                        "color": "#000000",
                        "flex": 1,
                        "gravity": "top",
                        "margin": "md",
                        "size": "sm",
                        "text": "設定 : r 次",
                        "type": "text",
                        "weight": "regular",
                        "wrap": True
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "align": "end",
                        "color": "#aaaaaa",
                        "flex": 1,
                        "gravity": "top",
                        "margin": "sm",
                        "size": "xs",
                        "text": "2019/03/08 21:00",
                        "type": "text",
                        "weight": "regular",
                        "wrap": True
                    }
                    ],
                    "flex": 1,
                    "layout": "vertical",
                    "margin": "md",
                    "spacing": "md",
                    "type": "box"
                },
                "hero": {
                    "aspectMode": "cover",
                    "aspectRatio": "20:13",
                    "size": "full",
                    "type": "image",
                    "url": "https://i.imgur.com/GIrEMgY.png"
                },
                "type": "bubble"
                },
                "type": "flex"
            }
        ]

    def test_lassie_alarm_message(self):
        self.assertEquals(
            json.loads(str(self.result_message)),
            self.expected_message
        )