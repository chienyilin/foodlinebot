# -*- coding: utf-8 -*-
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
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
handler = WebhookHandler('1441b0c3a47a16b4205287848d9daa91')

line_bot_api.push_message('U26e6062efb6aacd3b61e235ce67a0587', TextSendMessage(text='你可以開始了'))

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
        events = handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    for event in events:
        if isinstance(event.message, MessageEvent):
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
            if event.postback.data[0:1] == 'A' or event.postback.data[0:1] == 'B':
                shoptype = event.postback.data[2:]
                #if shoptype != '餐廳':
                line_bot_api.reply_message(   # 回復「選擇價位類別」按鈕樣板訊息
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='Price',
                            text='請選擇價位',
                            actions=[
                                PostbackTemplateAction(  # 將第一步驟選擇的餐廳，包含在第二步驟的資料中
                                    label='$0~$100',
                                    text='低價位',
                                    data='C&' + shoptype + '&低價位'
                                ),
                                PostbackTemplateAction(
                                    label='$100-$300',
                                    text='中價位',
                                    data='C&' + shoptype + '&中價位'
                                ),
                                PostbackTemplateAction(
                                    label='$300以上',
                                    text='高價位',
                                    data='C&' + shoptype + '&高價位'
                                )
                            ]
                        )
                    )
                )
            elif event.postback.data[0:1] == "C":
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
                                    label='3.5星以上',
                                    text='簡簡單單',
                                    data='D&' + shoptype + '&' + pricechoice + '&3.5星以上'
                                ),
                                PostbackTemplateAction(
                                    label='4星以上',
                                    text='來間好一點的',
                                    data='D&' + shoptype + '&' + pricechoice + '&4星以上'
                                ),
                                PostbackTemplateAction(
                                    label='4.5星以上',
                                    text='真嚴格',
                                    data='D&' + shoptype + '&' + pricechoice + '&4.5星以上'
                                )
                            ]
                        )
                    )
                )
                
                
    #else:
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)