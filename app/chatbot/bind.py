'''
LINE account with Goodlinker AWS user

Created at 2018/12/26 by Eric
'''
from linebot.models import TextSendMessage

from .. import db
from ..models import Member, User


# Check user is bind
def check_bind(line_user_id):
    user = User.query.filter_by(line_user_id=line_user_id).first()
    if user:
        return True
    return False

def bind_member(line_user_id, source_id, source_type):
    if not check_room_and_group_bind(source_id, source_type):
        user = User.query.filter_by(line_user_id=line_user_id).one()
        member = Member(
                user_id=user.id,
                source_id=source_id,
                source_type=source_type
            )
        db.session.add(member)
        try:
            db.session.commit()
        except:
            pass
        content = '綁定成功'
    else:
        content = '綁定失敗'
    return TextSendMessage(text=content)

def check_room_and_group_bind(source_id, source_type):
    user = Member.query.filter_by(
        source_id=source_id,
        source_type=source_type
    ).first()
    if user is None:
        return False
    return True

