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

class FourAlarmTestCase(unittest.TestCase):

    def setUp(self):

        output= [
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
                                                    "text": "v (偵測值)",
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
                                    "text": "設定 : r",
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

        self.lamp_result_message = lassie_alarm_message(self.mqtt_msg('lamp'))
        self.lamp_expected_message = output

        self.state_result_message = lassie_alarm_message(self.mqtt_msg('state'))
        self.state_expected_message = output

        self.color_result_message = lassie_alarm_message(self.mqtt_msg('color'))
        self.color_expected_message = output

        self.detector_result_message = lassie_alarm_message(self.mqtt_msg('detector'))
        self.detector_expected_message = output

    def mqtt_msg(self, alarmtype):
        return (
            {
                "t": alarmtype,
                "nt": "nt",
                "ns": "ns",
                "v": "v",
                "r": "r",
                "url": "",
                "time": "2019/03/08 21:00",
                "u": "3413f2a4-9663-4c34-95c9-b0399bb8d884"
            }
        )



    def test_four_alarm_type(self):
        self.assertEquals(
            json.loads(str(self.lamp_result_message)),
            self.lamp_expected_message
        )
        self.assertEquals(
            json.loads(str(self.state_result_message)),
            self.state_expected_message
        )
        self.assertEquals(
            json.loads(str(self.color_result_message)),
            self.color_expected_message
        )
        self.assertEquals(
            json.loads(str(self.detector_result_message)),
            self.detector_expected_message
        )



class AlarmCurrentTestCase(unittest.TestCase):
    def setUp(self):
        self.data = {
              "t": "current",
              "nt": "nt",
              "ns": "ns",
              "v": "v",
              "r": "r",
              "url": "",
              "time": "2019/03/08 21:00",
              "u": "3413f2a4-9663-4c34-95c9-b0399bb8d884"
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
                                    "text": "v (mAh)",
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
                            "text": "設定 : r mAh",
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

    def test_lassie_current_alarm_message(self):
        self.assertEquals(
            json.loads(str(self.result_message)),
            self.expected_message
        )


class AlarmTemperatureTestCase(unittest.TestCase):
    def setUp(self):
        self.data = {
              "t": "temperature",
              "nt": "加工區",
              "ns": "一號機溫度",
              "v": 27.2,
              "r": 10000,
              "url": "",
              "time": "2018-10-22T10:43:58",
              "u": "3413f2a4-9663-4c34-95c9-b0399bb8d884",
              "s": "alarm",
              "ra": {
                "h": 27,
                "l": 15
              },
              "vc": "red"
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
                                    "text": "27.2 (℃)",
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
                            "text": "設定 : 27 ～ 15 ℃",
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
                    },
                    "type": "flex"
                  }
                ]

    def test_lassie_temperature_alarm_message(self):
        self.assertEquals(
            json.loads(str(self.result_message)),
            self.expected_message
        )



class AlarmHumidityTestCase(unittest.TestCase):
    def setUp(self):
        self.data = {
              "t": "humidity",
              "nt": "加工區",
              "ns": "一號機溫度",
              "v": 27.2,
              "r": 10000,
              "url": "",
              "time": "2018-10-22T10:43:58",
              "u": "3413f2a4-9663-4c34-95c9-b0399bb8d884",
              "s": "alarm",
              "ra": {
                "h": 27,
                "l": 15
              },
              "vc": "red"
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
                                    "text": "27.2 (%)",
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
                            "text": "設定 : 27 ～ 15 %",
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
                    },
                    "type": "flex"
                  }
                ]

    def test_lassie_humidity_alarm_message(self):
        self.assertEquals(
            json.loads(str(self.result_message)),
            self.expected_message
        )



class AlarmTimerTestCase(unittest.TestCase):
    def setUp(self):
        self.data = {
              "t": "timer",
              "nt": "加工區",
              "ns": "一號機溫度",
              "v": 27.2,
              "r": 10000,
              "url": "",
              "time": "2018-10-22T10:43:58",
              "u": "3413f2a4-9663-4c34-95c9-b0399bb8d884",
              "s": "alarm",
              "ra": {
                "h": 27,
                "l": 15
              },
              "vc": "red"
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
                                    "text": "27.2 (秒)",
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
                            "text": "設定 : 10000 秒",
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
                    },
                    "type": "flex"
                  }
                ]

    def test_lassie_timer_alarm_message(self):
        self.assertEquals(
            json.loads(str(self.result_message)),
            self.expected_message
        )


class AlarmOcrTestCase(unittest.TestCase):
    def setUp(self):
        self.data = {
              "t": "ocr",
              "nt": "加工區",
              "ns": "一號機溫度",
              "v": 27.2,
              "r": 10000,
              "url": "https://i.imgur.com/Hn6lBtg.jpg",
              "time": "2018-10-22T10:43:58",
              "u": "3413f2a4-9663-4c34-95c9-b0399bb8d884",
              "s": "alarm",
              "ra": {
                "h": 27,
                "l": 15
              },
              "vc": "red"
            }
        self.result_message = lassie_alarm_message(self.data)
        self.expected_message = [
                  {
                    "type": "image",
                    "originalContentUrl": "https://i.imgur.com/Hn6lBtg.jpg",
                    "previewImageUrl": "https://i.imgur.com/Hn6lBtg.jpg"
                  },
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
                                    "text": "27.2(偵測值)",
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
                            "text": "設定 : 27 ～ 15",
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
                    },
                    "type": "flex"
                  }
                ]

    def test_lassie_ocr_alarm_message(self):
        self.assertEquals(
            json.loads(str(self.result_message)),
            self.expected_message
        )