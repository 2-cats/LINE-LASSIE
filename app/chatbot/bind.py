'''
LINE account with Goodlinker AWS user

Created at 2018/12/26 by Eric
'''

from ..models import User,member
from .. import db

#import pymysql

# Check user is bind
def check_bind(line_user_id):
    user = User.query.filter_by(line_user_id=line_user_id).first()
    if user:
        return True
    return False


# Bind user to RDS table: members
def bind_room_or_group_id(source_id,source_type, line_user_id):

    member = member(source_id=source_id,source_type=source_type, line_user_id=line_user_id)
    db.session.add(member)
    try:
        db.session.commit()
    except:
        pass
