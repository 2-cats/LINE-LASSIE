import json
import unittest
import datetime
import responses
from linebot import LineBotApi

from app.chatbot.abnormal import (get_device_list_data_for_alarmlist, have_device_message_for_alarmlist,
                                no_device_message_for_alarmlist,summary)


class DeviceDataTestCaseForAbnormal(unittest.TestCase):
    '''
    Test device
    '''

    def setUp(self):
        '''
        Set up test
        '''
        # test data
        self.result_message = get_device_list_data_for_alarmlist('Ud739a32831d46aa18507233eb0a68e60')
        self.expected_message = [
            {'name': 'GL01', 'display_name': 'GL01'},
            {'name': 'PI001', 'display_name': 'PI001'},
             {'name': 'PI001Fake', 'display_name': 'P1001Fake'},
             {'name': 'LassieDrawTest', 'display_name': 'LassieDrawTest'}
        ]

    def test_get_device_list_data_for_alarmlist(self):
        self.assertEquals(self.result_message, self.expected_message)

class NoDeviceDataTestCaseForAbnormal(unittest.TestCase):
    '''
    Test device
    '''

    def setUp(self):
        '''
        Set up test
        '''
        # test data
        self.result_message = get_device_list_data_for_alarmlist('line_user_id')
        self.expected_message = [

        ]
    def test_get_device_list_data_for_alarmlist(self):
        self.assertEquals(self.result_message, self.expected_message)



class HaveDeviceMessageTestCaseForAbnormal(unittest.TestCase):
    '''
    Test device
    '''

    def setUp(self):
        '''
        Set up test
        '''
        self.tested = LineBotApi('channel_secret')
        # test data


        self.result_message = have_device_message_for_alarmlist(
            'Ud739a32831d46aa18507233eb0a68e60',
            [
            {'name': 'GL01', 'display_name': 'GL01'}
             ]
        )
        self.expected_message = [
            {
                "altText": "異常設備清單",
                "contents": {
                    "contents": [
                        {
                            "body": {
                                "contents": [
                                    {
                                        "size": "lg",
                                        "text": "GL01",
                                        "type": "text",
                                        "weight": "bold",
                                        "wrap": True
                                    },
                                    {
                                        "action": {
                                            "data": "abnormal,GL01",
                                            "displayText": "查詢異常總覽...",
                                            "label": "異常總表",
                                            "type": "postback"
                                        },
                                        "flex": 100,
                                        "gravity": "center",
                                        "height": "sm",
                                        "style": "link",
                                        "type": "button"
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
        ]
    @responses.activate
    def test_have_device_message_for_alarmlist(self):
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




class NoDeviceMessageTestCaseForAbnormal(unittest.TestCase):
    '''
    Test device
    '''

    def setUp(self):
        '''
        Set up test
        '''
        self.tested = LineBotApi('channel_secret')
        # test data
        self.result_message = no_device_message_for_alarmlist('line_user_id')
        self.expected_message = [
            {
                "text": "搜尋不到任何萊西！",
                "type": "text"
            }
        ]

    @responses.activate
    def test_no_device_message_for_alarmlist(self):
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
class SummaryForAbnormal(unittest.TestCase):
    '''
    Test device
    '''

    def setUp(self):
        '''
        Set up test
        '''
        self.tested = LineBotApi('channel_secret')
        # test data
        data="abnormal,PI001Fake"
        # Convet to postback_data: [action, var1, var2, ... ,varN]
        test = data.split(",")
        self.result_message = summary('Ud739a32831d46aa18507233eb0a68e60',test)
        self.expected_message = [
            {
                "altText": "異常總表",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "contents": [
                            {
                                "contents": [
                                    {
                                        "color": "#030303",
                                        "size": "lg",
                                        "text": "Sensor",
                                        "type": "text",
                                        "weight": "bold"
                                    },
                                    {
                                        "align": "end",
                                        "color": "#030303",
                                        "margin": "md",
                                        "size": "lg",
                                        "text": "Value",
                                        "type": "text",
                                        "weight": "bold"
                                    }
                                ],
                                "flex": 1,
                                "layout": "horizontal",
                                "margin": "md",
                                "spacing": "sm",
                                "type": "box"
                            },
                            {
                                "type": "separator"
                            },
                            {
                                "contents": [
                                    {
                                        "contents": [
                                            {
                                                "color": "#555555",
                                                "margin": "md",
                                                "text": "燈號2",
                                                "type": "text"
                                            },
                                            {
                                                "align": "end",
                                                "color": "#555555",
                                                "flex": 0,
                                                "margin": "md",
                                                "text": "red",
                                                "type": "text"
                                            }
                                        ],
                                        "flex": 1,
                                        "layout": "horizontal",
                                        "margin": "md",
                                        "spacing": "sm",
                                        "type": "box"
                                    },
                                    {
                                        "contents": [
                                            {
                                                "color": "#555555",
                                                "margin": "md",
                                                "text": "計時2",
                                                "type": "text"
                                            },
                                            {
                                                "align": "end",
                                                "color": "#555555",
                                                "flex": 0,
                                                "margin": "md",
                                                "text": "100",
                                                "type": "text"
                                            }
                                        ],
                                        "flex": 1,
                                        "layout": "horizontal",
                                        "margin": "md",
                                        "spacing": "sm",
                                        "type": "box"
                                    },
                                    {
                                        "contents": [
                                            {
                                                "color": "#555555",
                                                "margin": "md",
                                                "text": "計次3",
                                                "type": "text"
                                            },
                                            {
                                                "align": "end",
                                                "color": "#555555",
                                                "flex": 0,
                                                "margin": "md",
                                                "text": "1002",
                                                "type": "text"
                                            }
                                        ],
                                        "flex": 1,
                                        "layout": "horizontal",
                                        "margin": "md",
                                        "spacing": "sm",
                                        "type": "box"
                                    },
                                    {
                                        "contents": [
                                            {
                                                "color": "#555555",
                                                "margin": "md",
                                                "text": "偵測3",
                                                "type": "text"
                                            },
                                            {
                                                "align": "end",
                                                "color": "#555555",
                                                "flex": 0,
                                                "margin": "md",
                                                "text": "1",
                                                "type": "text"
                                            }
                                        ],
                                        "flex": 1,
                                        "layout": "horizontal",
                                        "margin": "md",
                                        "spacing": "sm",
                                        "type": "box"
                                    },
                                    {
                                        "contents": [
                                            {
                                                "color": "#555555",
                                                "margin": "md",
                                                "text": "濕度1",
                                                "type": "text"
                                            },
                                            {
                                                "align": "end",
                                                "color": "#555555",
                                                "flex": 0,
                                                "margin": "md",
                                                "text": "35.2",
                                                "type": "text"
                                            }
                                        ],
                                        "flex": 1,
                                        "layout": "horizontal",
                                        "margin": "md",
                                        "spacing": "sm",
                                        "type": "box"
                                    }
                                ],
                                "flex": 1,
                                "layout": "vertical",
                                "margin": "md",
                                "spacing": "sm",
                                "type": "box"
                            },
                            {
                                "type": "separator"
                            },
                            {
                                "contents": [
                                    {
                                        "align": "start",
                                        "color": "#aaaaaa",
                                        "gravity": "top",
                                        "size": "xs",
                                        "text": "Date",
                                        "type": "text",
                                        "weight": "regular"
                                    },
                                    {
                                        "align": "end",
                                        "color": "#aaaaaa",
                                        "gravity": "top",
                                        "margin": "md",
                                        "size": "xs",
                                        "text": (datetime.datetime.now() + datetime.timedelta(hours=0)).strftime(
                                            '%Y-%m-%d %H:%M:%S'),
                                        "type": "text",
                                        "weight": "regular"
                                    }
                                ],
                                "flex": 1,
                                "layout": "horizontal",
                                "margin": "md",
                                "spacing": "sm",
                                "type": "box"
                            }
                        ],
                        "flex": 1,
                        "layout": "vertical",
                        "margin": "md",
                        "spacing": "sm",
                        "type": "box"
                    },
                    "direction": "ltr",
                    "header": {
                        "contents": [
                            {
                                "color": "#1DB446",
                                "margin": "md",
                                "size": "xxl",
                                "text": "Report",
                                "type": "text",
                                "weight": "bold",
                                "wrap": True
                            },
                            {
                                "color": "#aaaaaa",
                                "size": "xs",
                                "text": "PI001Fake",
                                "type": "text"
                            },
                            {
                                "type": "separator"
                            }
                        ],
                        "layout": "vertical",
                        "type": "box"
                    }
                },
                "type": "flex"
            }

        ]
        #self.maxDiff=None

    @responses.activate
    def test_summary(self):
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