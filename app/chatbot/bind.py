'''
LINE account with Goodlinker AWS user

Created at 2018/12/26 by Eric
'''

from ..models import User


# Check user is bind
def check_bind(line_user_id):
    user = User.query.filter_by(line_user_id=line_user_id).first()
    if user:
        return True
    return False
