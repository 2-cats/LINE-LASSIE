import json
import unittest

from flask import Flask

from app.chatbot.report import lassie_report_message

app = Flask(__name__)
app.config.from_pyfile("../instance/config.py")


class ReportTestCase(unittest.TestCase):
    def setUp(self):
        self.data = {
            'u': 'aws_user_name',
            'x': '一號溫度機',
            'd': "一號溫度機,5 , 1, 2,  4, 0, 4, 6, 5, 1,  2, 4, 0, 4, 6, 5, 1, 2, 4, 0, 4, 6, 5, 1, 3"
        }
        self.result_message = lassie_report_message(self.data)
        self.expected_message = {
            "altText": "一號溫度機 的今日報表",
            "contents": {
                "body": {
                "contents": [
                    {
                    "color": "#1DB446",
                    "size": "lg",
                    "text": "一號溫度機 的今日報表",
                    "type": "text",
                    "weight": "bold",
                    "wrap": True
                    },
                    {
                    "size": "md",
                    "text": "我已經幫你整理完成了，請點擊檢視",
                    "type": "text",
                    "wrap": True
                    }
                ],
                "flex": 1,
                "layout": "vertical",
                "margin": "md",
                "spacing": "md",
                "type": "box"
                },
                "footer": {
                "contents": [
                    {
                    "action": {
                        "label": "檢視報表",
                        "type": "uri",
                        "uri": ''.join(
                            [
                                app.config['REPORT_LINE_LIFF_URL'],
                                "?data=%E4%B8%80%E8%99%9F%E6%BA%AB%E5%BA%A6%E6%A9%9F%2C5+%2C+1%2C+2%2C++4%2C+0%2C+4%2C+6%2C+5%2C+1%2C++2%2C+4%2C+0%2C+4%2C+6%2C+5%2C+1%2C+2%2C+4%2C+0%2C+4%2C+6%2C+5%2C+1%2C+3"
                            ]
                        )
                    },
                    "style": "link",
                    "type": "button"
                    }
                ],
                "flex": 1,
                "layout": "vertical",
                "margin": "md",
                "spacing": "md",
                "type": "box"
                },
                "type": "bubble"
            },
            "type": "flex"
            }
        
    
    def test_lassie_report_message(self):
        self.assertEquals(
            json.loads(str(self.result_message)),
            self.expected_message
        )
