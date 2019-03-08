import json
import unittest

from app import create_app, db
from app.chatbot.abnormal import (alarm_list_message, get_alarm_list_data,
                                  get_shadow, have_alarm_message,
                                  no_alarm_message, summary)
from app.models import User

class GetShadowTestCase(unittest.TestCase):
    def setUp(self):
        self.result_message = get_shadow('PI001')
        self.expected_message = {
            "state": {
                "reported": {
                "user": "fsdfwer2322",
                "devs": [
                    "lp01",
                    "lp02",
                    "t01",
                    "t02",
                    "t03",
                    "ct01",
                    "ct02",
                    "ct03",
                    "cou01",
                    "cou02",
                    "cou03",
                    "det01",
                    "det02",
                    "det03",
                    "tmp01",
                    "tmp02",
                    "tmp03",
                    "hum01",
                    "hum02",
                    "hum03",
                    "cam01"
                ],
                "errs": [
                    "lp02",
                    "t02",
                    "cou03",
                    "det03",
                    "hum01",
                    "cam01"
                ],
                "lp01": {
                    "n": "燈號1",
                    "r": "red",
                    "t": "lamp",
                    "s": "on",
                    "v": "green"
                },
                "lp02": {
                    "t": "lamp",
                    "n": "燈號2",
                    "r": "red",
                    "s": "alarm",
                    "v": "red"
                },
                "t01": {
                    "n": "計時1",
                    "r": "30",
                    "t": "timer",
                    "s": "on",
                    "v": "11"
                },
                "t02": {
                    "n": "計時2",
                    "r": "30",
                    "t": "timer",
                    "s": "alarm",
                    "v": "100"
                },
                "t03": {
                    "n": "計時3",
                    "r": "200",
                    "t": "timer",
                    "s": "on",
                    "v": "160"
                },
                "ct01": {
                    "n": "電流1",
                    "r": {
                    "l": "40",
                    "h": "100",
                    "z": "1"
                    },
                    "t": "current",
                    "s": "on",
                    "v": "60"
                },
                "ct02": {
                    "n": "電流2",
                    "r": {
                    "l": "40",
                    "h": "100",
                    "z": "1"
                    },
                    "t": "current",
                    "s": "on",
                    "v": "50"
                },
                "ct03": {
                    "n": "電流3",
                    "r": {
                    "l": "40",
                    "h": "100",
                    "z": "1"
                    },
                    "t": "current",
                    "s": "on",
                    "v": "41"
                },
                "cou01": {
                    "n": "計次1",
                    "r": "1000",
                    "t": "counter",
                    "s": "on",
                    "v": "101"
                },
                "cou02": {
                    "n": "計次2",
                    "r": "1000",
                    "t": "counter",
                    "s": "on",
                    "v": "500"
                },
                "cou03": {
                    "n": "計次3",
                    "r": "1000",
                    "t": "counter",
                    "s": "alarm",
                    "v": "1002"
                },
                "det01": {
                    "n": "偵測1",
                    "r": "1",
                    "t": "detector",
                    "s": "on",
                    "v": "0"
                },
                "det02": {
                    "n": "偵測2",
                    "r": "1",
                    "t": "detector",
                    "s": "on",
                    "v": "0"
                },
                "det03": {
                    "n": "偵測3",
                    "r": "1",
                    "t": "detector",
                    "s": "alarm",
                    "v": "1"
                },
                "tmp01": {
                    "n": "溫度1",
                    "r": {
                    "l": "15",
                    "h": "27"
                    },
                    "t": "temperature",
                    "s": "on",
                    "v": "25.3"
                },
                "tmp02": {
                    "n": "溫度2",
                    "r": {
                    "l": "15",
                    "h": "27"
                    },
                    "t": "temperature",
                    "s": "on",
                    "v": "26.0"
                },
                "tmp03": {
                    "n": "溫度3",
                    "r": {
                    "l": "15",
                    "h": "27"
                    },
                    "t": "temperature",
                    "s": "on",
                    "v": "25.2"
                },
                "hum01": {
                    "n": "濕度1",
                    "r": {
                    "l": "40",
                    "h": "60"
                    },
                    "t": "humidity",
                    "s": "alarm",
                    "v": "35.2"
                },
                "hum02": {
                    "n": "濕度2",
                    "r": {
                    "l": "40",
                    "h": "60"
                    },
                    "t": "humidity",
                    "s": "on",
                    "v": "40.2"
                },
                "hum03": {
                    "n": "濕度3",
                    "r": {
                    "l": "40",
                    "h": "60"
                    },
                    "t": "humidity",
                    "s": "on",
                    "v": "50"
                },
                "cam01": {
                    "devs": [
                    "surv01",
                    "surv02",
                    "surv03"
                    ],
                    "errs": [
                    "surv03"
                    ],
                    "s": "alarm",
                    "surv01": {
                    "n": "機台一完成度",
                    "r": {
                        "l": "0",
                        "h": "100"
                    },
                    "t": "ocr",
                    "s": "on",
                    "v": "90.2",
                    "size": {
                        "x": 1024,
                        "y": 768
                    },
                    "roi": {
                        "x": 50,
                        "y": 150,
                        "w": 200,
                        "h": 100
                    }
                    },
                    "surv02": {
                    "n": "機台警示顏色",
                    "r": "red",
                    "t": "color",
                    "s": "on",
                    "v": "green",
                    "size": {
                        "x": 1024,
                        "y": 768
                    },
                    "roi": {
                        "x": 50,
                        "y": 50,
                        "w": 200,
                        "h": 100
                    }
                    },
                    "surv03": {
                    "n": "機台一次數",
                    "r": {
                        "l": "0",
                        "h": "100"
                    },
                    "t": "ocr",
                    "s": "alarm",
                    "v": "101",
                    "url": "https://i.imgur.com/Hn6lBtg.jpg",
                    "size": {
                        "x": 1024,
                        "y": 768
                    },
                    "roi": {
                        "x": 50,
                        "y": 150,
                        "w": 200,
                        "h": 100
                    }
                    },
                    "n": "機台一畫面監控"
                },
                "n": "一樓加工區"
                }
            },
            "metadata": {
                "reported": {
                "user": {
                    "timestamp": 1548325750
                },
                "devs": [
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    }
                ],
                "errs": [
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    },
                    {
                    "timestamp": 1548325750
                    }
                ],
                "lp01": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "timestamp": 1548325750
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "lp02": {
                    "t": {
                    "timestamp": 1548325750
                    },
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "t01": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "timestamp": 1548325750
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "t02": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "timestamp": 1548325750
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "t03": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "timestamp": 1548325750
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "ct01": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "l": {
                        "timestamp": 1548325750
                    },
                    "h": {
                        "timestamp": 1548325750
                    },
                    "z": {
                        "timestamp": 1548325750
                    }
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "ct02": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "l": {
                        "timestamp": 1548325750
                    },
                    "h": {
                        "timestamp": 1548325750
                    },
                    "z": {
                        "timestamp": 1548325750
                    }
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "ct03": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "l": {
                        "timestamp": 1548325750
                    },
                    "h": {
                        "timestamp": 1548325750
                    },
                    "z": {
                        "timestamp": 1548325750
                    }
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "cou01": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "timestamp": 1548325750
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "cou02": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "timestamp": 1548325750
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "cou03": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "timestamp": 1548325750
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "det01": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "timestamp": 1548325750
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "det02": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "timestamp": 1548325750
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "det03": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "timestamp": 1548325750
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "tmp01": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "l": {
                        "timestamp": 1548325750
                    },
                    "h": {
                        "timestamp": 1548325750
                    }
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "tmp02": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "l": {
                        "timestamp": 1548325750
                    },
                    "h": {
                        "timestamp": 1548325750
                    }
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "tmp03": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "l": {
                        "timestamp": 1548325750
                    },
                    "h": {
                        "timestamp": 1548325750
                    }
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "hum01": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "l": {
                        "timestamp": 1548325750
                    },
                    "h": {
                        "timestamp": 1548325750
                    }
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "hum02": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "l": {
                        "timestamp": 1548325750
                    },
                    "h": {
                        "timestamp": 1548325750
                    }
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "hum03": {
                    "n": {
                    "timestamp": 1548325750
                    },
                    "r": {
                    "l": {
                        "timestamp": 1548325750
                    },
                    "h": {
                        "timestamp": 1548325750
                    }
                    },
                    "t": {
                    "timestamp": 1548325750
                    },
                    "s": {
                    "timestamp": 1548325750
                    },
                    "v": {
                    "timestamp": 1548325750
                    }
                },
                "cam01": {
                    "devs": [
                    {
                        "timestamp": 1548325750
                    },
                    {
                        "timestamp": 1548325750
                    },
                    {
                        "timestamp": 1548325750
                    }
                    ],
                    "errs": [
                    {
                        "timestamp": 1548325750
                    }
                    ],
                    "s": {
                    "timestamp": 1548325750
                    },
                    "surv01": {
                    "n": {
                        "timestamp": 1548325750
                    },
                    "r": {
                        "l": {
                        "timestamp": 1548325750
                        },
                        "h": {
                        "timestamp": 1548325750
                        }
                    },
                    "t": {
                        "timestamp": 1548325750
                    },
                    "s": {
                        "timestamp": 1548325750
                    },
                    "v": {
                        "timestamp": 1548325750
                    },
                    "size": {
                        "x": {
                        "timestamp": 1548325750
                        },
                        "y": {
                        "timestamp": 1548325750
                        }
                    },
                    "roi": {
                        "x": {
                        "timestamp": 1548325750
                        },
                        "y": {
                        "timestamp": 1548325750
                        },
                        "w": {
                        "timestamp": 1548325750
                        },
                        "h": {
                        "timestamp": 1548325750
                        }
                    }
                    },
                    "surv02": {
                    "n": {
                        "timestamp": 1548325750
                    },
                    "r": {
                        "timestamp": 1548325750
                    },
                    "t": {
                        "timestamp": 1548325750
                    },
                    "s": {
                        "timestamp": 1548325750
                    },
                    "v": {
                        "timestamp": 1548325750
                    },
                    "size": {
                        "x": {
                        "timestamp": 1548325750
                        },
                        "y": {
                        "timestamp": 1548325750
                        }
                    },
                    "roi": {
                        "x": {
                        "timestamp": 1548325750
                        },
                        "y": {
                        "timestamp": 1548325750
                        },
                        "w": {
                        "timestamp": 1548325750
                        },
                        "h": {
                        "timestamp": 1548325750
                        }
                    }
                    },
                    "surv03": {
                    "n": {
                        "timestamp": 1548325750
                    },
                    "r": {
                        "l": {
                        "timestamp": 1548325750
                        },
                        "h": {
                        "timestamp": 1548325750
                        }
                    },
                    "t": {
                        "timestamp": 1548325750
                    },
                    "s": {
                        "timestamp": 1548325750
                    },
                    "v": {
                        "timestamp": 1548325750
                    },
                    "url": {
                        "timestamp": 1548325750
                    },
                    "size": {
                        "x": {
                        "timestamp": 1548325750
                        },
                        "y": {
                        "timestamp": 1548325750
                        }
                    },
                    "roi": {
                        "x": {
                        "timestamp": 1548325750
                        },
                        "y": {
                        "timestamp": 1548325750
                        },
                        "w": {
                        "timestamp": 1548325750
                        },
                        "h": {
                        "timestamp": 1548325750
                        }
                    }
                    },
                    "n": {
                    "timestamp": 1548325750
                    }
                },
                "n": {
                    "timestamp": 1548325750
                }
                }
            },
            "version": 80,
            "timestamp": 1552022499
            }

    def test_get_device_data(self):
        self.assertEqual(
            self.result_message,
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
                "display_name": "PI001"
            },
            {
                "name": "test_02",
                "display_name": "PI001"
            }
        ]
        self.result_message = have_alarm_message(self.devices_data)
        self.expected_message = {
            "altText": "異常設備清單",
            "contents": {
                "contents": [
                {
                    "body": {
                    "contents": [
                        {
                        "size": "lg",
                        "text": "PI001",
                        "type": "text",
                        "weight": "bold",
                        "wrap": True
                        },
                        {
                        "action": {
                            "data": "abnormal,test_01",
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
                },
                {
                    "body": {
                    "contents": [
                        {
                        "size": "lg",
                        "text": "PI001",
                        "type": "text",
                        "weight": "bold",
                        "wrap": True
                        },
                        {
                        "action": {
                            "data": "abnormal,test_02",
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

    def test_have_device_message(self):
        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )

class NoDeviceTestCase(unittest.TestCase):
    def setUp(self):
        '''
        Set up test
        '''
        # test data
        self.result_message = no_alarm_message()
        self.expected_message = {
            'text': '搜尋不到任何萊西！',
            'type': 'text'
        }

    def test_no_device_message(self):
        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )

class GetDeviceDataTestCase(unittest.TestCase):
    def setUp(self):
        '''
        Set up test
        '''
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create fake User data
        user = User(
            line_user_id='line_user_id',
            aws_user_name='aws_user_name'
        )

        db.session.add_all([user])
        db.session.commit()

        self.result_message = get_alarm_list_data(user.line_user_id)
        self.expected_message = [
            {
                'name': 'PI001',
                'display_name': 'PI001'
            },
            {
                'name': 'PI001',
                'display_name': 'PI001'
            }
        ]

    def tearDown(self):
        db.session.remove()  # Remove database session
        db.drop_all()  # Drop database
        self.app_context.pop()

    def test_get_device_data(self):
        self.assertEqual(
            self.result_message,
            self.expected_message
        )
