from linebot.models import (BoxComponent, BubbleContainer, ButtonComponent,
                            FlexSendMessage, TextComponent, TextSendMessage,
                            URIAction)


def contact_us(line_user_id):
    bubble = BubbleContainer(
        direction='ltr',
        body=BoxComponent(
            layout='vertical',
            flex=1,
            spacing='sm',
            margin='md',
            contents=[
                TextComponent(
                    text='遇到問題？',
                    weight='bold',
                    wrap=True,
                    color='#17c950',
                    size='xl',
                ),
                TextComponent(
                    text='如果在使用上遇到問題，歡迎直接聯繫我們的客服！',
                    wrap=True,
                    size='lg',
                    margin='md',
                )
            ]
        ),
        footer=BoxComponent(
            layout='vertical',
            flex=1,
            spacing='sm',
            margin='md',
            contents=[
                ButtonComponent(
                    style='link',
                    action=URIAction(
                        label='電話客服',
                        uri='tel:02-82315949'
                    )
                )
            ]
        )
    )
    message = FlexSendMessage(alt_text='遇到問題', contents=bubble)
    return message
