import datetime
from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            FlexSendMessage, TextComponent)

from ..models import User


def follow_message():
    bubble_template = BubbleContainer(
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                    text='歡迎加入',
                    wrap=True,
                    weight='bold',
                    size='lg',
                ),
                TextComponent(
                    text='您好，我是 Lassie！我致力於打造一個連結各種設備與用戶之間聰明、可靠、友善的互動系統，讓用戶能隨時掌握設備狀況建立連結！第一次使用請先完成綁定喔！',
                    wrap=True,
                    size='md',
                    margin='md'
                )
            ]
        )
    )
    message = FlexSendMessage(
        alt_text='歡迎您的加入',
        contents=bubble_template
    )
    return message

def unfollow(line_user_id):
    user = User.query.filter_by(
        line_user_id=line_user_id,
        deleted_at=None
    ).first()
    user.deleted_at = datetime.datetime.now()
    if user:
        db.session.add(user)

        try:
            User.link_rm_to_guest(user)
        except:
            pass

        try:
            db.session.commit()
        except:
            pass
