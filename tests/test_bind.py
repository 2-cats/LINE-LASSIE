import unittest

from app.chatbot.bind import check_bind

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.bind_user_lind_id = "Ud70573ef58ee136041925101bc130d72"
        self.unbind_user_lind_id = "line_user_id"

    def test_check_bind(self):
        self.assertEquals(check_bind(self.bind_user_lind_id), True)
        self.assertEquals(check_bind(self.unbind_user_lind_id), False)