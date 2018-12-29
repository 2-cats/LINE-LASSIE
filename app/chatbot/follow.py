from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            FlexSendMessage, TextComponent)
from .richmenu import link_rm_to_guest

def follow_message(line_user_id):
    bubble_template = BubbleContainer(
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                    text='歡迎加入',
                    wrap=True,
                    weight= 'bold',
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
        alt_text='抱歉，我聽不懂指令', contents=bubble_template)
    return message

def unfollow(line_user_id):
    link_rm_to_guest(line_user_id)