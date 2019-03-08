import json
import unittest

from app.chatbot.contact import contact_us


class ContactTestCase(unittest.TestCase):
    '''
    Test contact
    '''
    def setUp(self):
        '''
        Set up test
        '''
        # test data
        self.result_message = contact_us('line_user_id')
        self.expected_message = {
            "altText":"遇到問題",
            "type":"flex",
            "contents":{
                "body":{
                    "contents":[
                        {
                            "color":"#17c950",
                            "size":"xl",
                            "text":"遇到問題？",
                            "type":"text",
                            "weight":"bold",
                            "wrap":True
                        },
                        {
                            "margin":"md",
                            "size":"lg",
                            "text":"如果在使用上遇到問題，歡迎直接聯繫我們的客服！",
                            "type":"text",
                            "wrap":True
                        }
                    ],
                    "flex":1,
                    "layout":"vertical",
                    "margin":"md",
                    "spacing":"sm",
                    "type":"box"
                },
                "direction":"ltr",
                "type":"bubble",
                "footer":{
                    "contents":[
                        {
                            "action":{
                                "label":"LINE@ 客服",
                                "type":"uri",
                                "uri":"line://ti/p/@gtb6688a"
                            },
                            "style":"link",
                            "type":"button"
                        },
                        {
                            "action":{
                                "label":"電話客服",
                                "type":"uri",
                                "uri":"tel:02-82315949"
                            },
                            "style":"link",
                            "type":"button"
                        }
                    ],
                    "layout":"vertical",
                    "margin":"md",
                    "type":"box"
                }
            }
        }

    def test_contact_message(self):
        '''
        Test reply contact event message
        '''
        self.assertEqual(
            json.loads(str(self.result_message)),
            self.expected_message
        )
