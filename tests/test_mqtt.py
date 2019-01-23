import json
import unittest

import responses
from linebot import LineBotApi

from app.mqtt.report import lassie_report_message
from app.mqtt.alarm import lassie_alarm_message,get_push_id

class MQTTTestCase(unittest.TestCase):
    def setUp(self):
        self.tested = LineBotApi('channel_secret')

        self.user_lind_id = "13a9cf07-b1c9-498d-80b3-47b95b6671c4"

        self.result_lassie_report_message = lassie_report_message("\"thing01 - 一號溫度機\",5")
        self.expected_lassie_report_message = [
            {
                "type":"flex",
                "altText":"今日報表",
                "contents":{
                    'type': 'bubble',
                    "body":{
                        "flex":1,
                        "layout":"vertical",
                        "margin":"md",
                        "spacing":"md",
                        "type":"box",
                        "contents":[
                            {
                                "color":"#1DB446",
                                "size":"lg",
                                "text":"今日報表",
                                "type":"text",
                                "weight":"bold"
                            },
                            {
                                "size":"md",
                                "text":"我已經幫你把今日報表整理完成了，請點擊檢視",
                                "type":"text",
                                "wrap":True
                            }
                        ]
                    },
                    "footer":{
                        "flex":1,
                        "layout":"vertical",
                        "margin":"md",
                        "spacing":"md",
                        "type":"box",
                        "contents":[
                            {
                                "action":{
                                    "label":"檢視報表",
                                    "type":"uri",
                                    "uri":"line://app/1633151989-ovydbgML?data=%22thing01+-+%E4%B8%80%E8%99%9F%E6%BA%AB%E5%BA%A6%E6%A9%9F%22%2C5"
                                },
                                "style":"link",
                                "type":"button"
                            }
                        ],
                        
                    },
                }
            }
        ]

    @responses.activate
    def test_lassie_report_message(self):
        '''
        Test reply lassie report message
        '''
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply',
            json={}, status=200
        )

        self.tested.reply_message('replyToken', self.result_lassie_report_message)
        
        request = responses.calls[0].request
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply')
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            json.loads(request.body),
            {
                'replyToken': 'replyToken',
                'messages': self.expected_lassie_report_message
            }
        )

class LassieAlarmMessageForNormal(unittest.TestCase):
    '''
    Test device
    '''

    def setUp(self):
        '''
        Set up test
        '''
        self.tested = LineBotApi('channel_secret')
        # test data
        self.result_message = lassie_alarm_message(

                {
                "time": "2018-10-22T10:43:58",
                 "s": "alarm",
                 "ra": {
                     "h": 27,
                     "l": 15
                 },
                 "r": 10000,
                 "url": "",
                 "u": "54ce49c7-9fc0-482d-850c-a39ae37f0d6c",
                 "nt": "加工區",
                 "ns": "一號機溫度",
                 "t": "counter",
                 "v": 27.2,
                 "vc": "red"
                 }

        )
        self.expected_message = [
            {
                "type": "flex",
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
                                "text": "加工區 異常",
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
                                                "text": "一號機溫度",
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
                                                "text": "27.2 (次)",
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
                                "text": "設定 : 10000 次",
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
                                "text": "2018-10-22T10:43:58",
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
                }
            }
        ]
        self.maxDiff=None

    @responses.activate
    def test_lassie_alarm_message(self):
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply',
            json={}, status=200
        )

        self.tested.reply_message('replyToken', self.result_message)

        request = responses.calls[0].request
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply')
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            json.loads(request.body),
            {
                'replyToken': 'replyToken',
                'messages': self.expected_message
            }
        )
class LassieAlarmMessageForCam(unittest.TestCase):
    '''
    Test device
    '''

    def setUp(self):
        '''
        Set up test
        '''
        self.tested = LineBotApi('channel_secret')
        # test data
        self.result_message = lassie_alarm_message(

                {
                "time": "2018-10-22T10:43:58",
                 "s": "alarm",
                 "ra": {
                     "h": 27,
                     "l": 15
                 },
                 "r": 10000,
                 "url": "https://truth.bahamut.com.tw/s01/201708/0e441d92e445dde641c86c8d235f14ca.JPG",
                 "u": "54ce49c7-9fc0-482d-850c-a39ae37f0d6c",
                 "nt": "加工區",
                 "ns": "一號機溫度",
                 "t": "counter",
                 "v": 27.2,
                 "vc": "red"
                 }

        )
        self.expected_message = [
            {
                "originalContentUrl": "https://truth.bahamut.com.tw/s01/201708/0e441d92e445dde641c86c8d235f14ca.JPG",
                "previewImageUrl": "https://truth.bahamut.com.tw/s01/201708/0e441d92e445dde641c86c8d235f14ca.JPG",
                "type": "image"
            },
            {
                "type": "flex",
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
                                "text": "加工區 異常",
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
                                                "text": "一號機溫度",
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
                                                "text": "27.2 (次)",
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
                                "text": "設定 : 10000 次",
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
                                "text": "2018-10-22T10:43:58",
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
                }
            }
        ]
        self.maxDiff=None

    @responses.activate
    def test_lassie_alarm_message(self):
        responses.add(
            responses.POST,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply',
            json={}, status=200
        )

        self.tested.reply_message('replyToken', self.result_message)

        request = responses.calls[0].request
        self.assertEqual(
            request.url,
            LineBotApi.DEFAULT_API_ENDPOINT + '/v2/bot/message/reply')
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            json.loads(request.body),
            {
                'replyToken': 'replyToken',
                'messages': self.expected_message
            }
        )
class GetPushId(unittest.TestCase):
    def setUp(self):
        self.result_message = get_push_id('54ce49c7-9fc0-482d-850c-a39ae37f0d6c')
        self.expected_message = 'Cd55d416e40dd3585fbcfd639de00994b'
    def test_get_push_id(self):
        self.assertEquals(self.result_message, self.expected_message)