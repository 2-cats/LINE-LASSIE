# import unittest


# from app import create_app, db
# from app.mqtt.user import (username_to_line_user_id)
# from app.models import User

# class BindTestCase(unittest.TestCase):

#     def setUp(self):
#         self.app = create_app('testing')
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()

#         # Create fake User data
#         user = User(
#             line_user_id='line_user_id',
#             aws_user_name='aws_user_name'
#         )

#         db.session.add_all([user])
#         db.session.commit()

#     def tearDown(self):
#         db.session.remove()  # Remove database session
#         db.drop_all()  # Drop database
#         self.app_context.pop()
    
#     def test_username_to_line_user_id(self):
#         self.assertEquals(
#             username_to_line_user_id('aws_user_name'),
#             'line_user_id'
#         )