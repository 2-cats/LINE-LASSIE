'''
LINE account with Goodlinker AWS user

Created at 2018/12/26 by Eric
'''
from linebot.models import ButtonsTemplate, TemplateSendMessage, URIAction


def bind_line_message(line_user_id):
    buttons_template = ButtonsTemplate(
        title='綁定服務',
        text='您好，我是 Lassie！第一次使用嗎？完成簡單的綁定只需要三分鐘，就可以享用完整的服務！',
        actions=[
            URIAction(
                label='點我進行綁定',
                uri='line://app/1633151989-5BJ0B9EZ'
            )
        ])
    template_message = TemplateSendMessage(
        alt_text='綁定帳號',
        template=buttons_template
    )
    return template_message

def check_bind_result(email, phone):
    return 'success'