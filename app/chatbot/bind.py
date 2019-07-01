'''
LINE account with Goodlinker AWS user

Created at 2018/12/26 by Eric
'''
from linebot.models import TextSendMessage

from .. import db
from ..models import Member, User

# Bind user from aws coginto
def bind_aws(aws_username, line_user_id):
    if len(aws_username)>15:
        if check_aws_bind_is_exist(aws_username):
            return TextSendMessage(text='這個使用者已經被綁定過')
        else:
            user = User(
                line_user_id=line_user_id,
                aws_user_name=aws_username
            )
            try:
                db.session.add(user)
                db.session.commit()
                User.link_rm_to_user(user)
                content = '綁定成功'
            except:
                content = '綁定失敗'
            return TextSendMessage(text=content)
    else:
        return TextSendMessage(text='糟糕，出了一些問題！')
    

# Check aws user is exist in database
def check_aws_bind_is_exist(aws_username):
    user = User.query.filter_by(
        aws_user_name=aws_username,
        deleted_at=None
    ).first()
    if user == None:
        return False
    return True

# Check user is bind
def check_bind(line_user_id):
    user = User.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()
    if user:
        return True
    return False

def bind_member(line_user_id, source_id, source_type):
    if check_room_and_group_bind(source_id, source_type):
        content = '綁定失敗'
    else:
        user = User.query.filter_by(
            line_user_id=line_user_id,
            deleted_at=None
        ).first()

        member = Member(
            user_id=user.id,
            source_id=source_id,
            source_type=source_type
        )
        db.session.add(member)
        try:
            db.session.commit()
            content = '綁定成功'
        except:
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
