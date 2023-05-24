# -*- coding: utf-8 -*-
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('5kd4nm3bDWl+WVCow3m0qje706VXFDrsSgB0QiB/ZOB2ZFIj5mXMYm6U6AAdh31+yIOY+sdNl9blhd0qijZl9lB7+W5l7jNZ+kOWbYG8tYDUY3MBk2nMu5nNN1XdfFY7VeAowBCB/GpOmhX8VganBAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
parser = WebhookParser('1441b0c3a47a16b4205287848d9daa91')

#line_bot_api.push_message('U26e6062efb6aacd3b61e235ce67a0587', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    for event in events:
        if isinstance(event, MessageEvent):
            message = event.message.text
            if message == "哈囉":
                line_bot_api.reply_message(
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='Category',
                            text='請選擇美食分類',
                            actions=[
                                PostbackTemplateAction(
                                    label='餐廳',
                                    text='餐廳',
                                    data='A&餐廳'
                                ),
                                PostbackTemplateAction(
                                    label='飲料店',
                                    text='飲料店',
                                    data='B&飲料店'
                                ),
                                PostbackTemplateAction(
                                    label='咖啡廳',
                                    text='咖啡廳',
                                    data='B&咖啡廳'
                                ),
                                PostbackTemplateAction(
                                    label='酒吧',
                                    text='酒吧',
                                    data='B&酒吧'
                                )
                            ]
                        )
                    )
                )
        elif isinstance(event,PostbackEvent):
            if event.postback.data[0:1] == 'A':
                flex_message=TextSendMessage(text="選擇你想要的餐廳類型",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(label="早午餐",text='早午餐',data="Q&早午餐")
                            ),
                        QuickReplyButton(
                            action=PostbackAction(label="中式",text='中式',data="Q&中式")
                            ),
                        QuickReplyButton(
                            action=PostbackAction(label="義式",text='義式',data="Q&義式")
                            ),
                        QuickReplyButton(
                            action=PostbackAction(label="日式",text='日式',data="Q&日式")
                            ),
                        QuickReplyButton(
                            action=PostbackAction(label="韓式",text='韓式',data="Q&韓式")
                            ),
                        QuickReplyButton(
                            action=PostbackAction(label="其他",text='其他',data="Q&其他")
                            ),
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, flex_message)
            elif event.postback.data[0:1] == 'Q':
                restaurant = event.postback.data[2:]
                line_bot_api.reply_message(   # 回復「選擇價位類別」按鈕樣板訊息
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='Price',
                            text='請選擇價位',
                            actions=[
                                PostbackTemplateAction(  # 將第一步驟選擇的餐廳，包含在第二步驟的資料中
                                    label='$0~$150',
                                    text='低價位',
                                    data='C&' + restaurant + '&低價位'
                                ),
                                PostbackTemplateAction(
                                    label='$150-$300',
                                    text='中價位',
                                    data='C&' + restaurant + '&中價位'
                                ),
                                PostbackTemplateAction(
                                    label='$300以上',
                                    text='高價位',
                                    data='C&' + restaurant + '&高價位'
                                )
                            ]
                        )
                    )
                )
            elif event.postback.data[0:1] == "B":
                shoptype = event.postback.data[2:]
                line_bot_api.reply_message(   # 回復「選擇評價類別」按鈕樣板訊息
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='reviews',
                            text='請選擇評價限制',
                            actions=[
                                PostbackTemplateAction(  # 將第一、二步驟選擇的餐廳，包含在第三步驟的資料中
                                    label='4星以上',
                                    text='簡簡單單',
                                    data='D&' + shoptype + '&4星以上'
                                ),
                                PostbackTemplateAction(
                                    label='4.5星以上',
                                    text='真嚴格',
                                    data='D&' + shoptype + '&4.5星以上'
                                ),
                                PostbackTemplateAction(
                                    label='隨機',
                                    text='都行',
                                    data='D&' + shoptype + '&隨機'
                                )
                            ]
                        )
                    )
                )
            elif event.postback.data[0:1] == "C":
                if '早午餐' in event.postback.data:
                    restaurant = event.postback.data[2:5]
                else:
                    restaurant = event.postback.data[2:4]
                pricechoice = event.postback.data[-3:]
                line_bot_api.reply_message(   # 回復「選擇評價類別」按鈕樣板訊息
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='reviews',
                            text='請選擇評價限制',
                            actions=[
                                PostbackTemplateAction(  # 將第一、二步驟選擇的餐廳，包含在第三步驟的資料中
                                    label='4星以上',
                                    text='簡簡單單',
                                    data='D&' + restaurant + '&' + pricechoice + '&4星以上'
                                ),
                                PostbackTemplateAction(
                                    label='4.5星以上',
                                    text='真嚴格',
                                    data='D&' + restaurant + '&' + pricechoice + '&4.5星以上'
                                ),
                                PostbackTemplateAction(
                                    label='隨機',
                                    text='都行',
                                    data='D&' + restaurant + '&' + pricechoice + '隨機'
                                )
                            ]
                        )
                    )
                )
                
    return 'ok'          
                
    #else:
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)