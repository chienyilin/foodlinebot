# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

@author: Ivan
版權屬於「行銷搬進大程式」所有若有疑問可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第四章 選單功能
按鈕樣板TemplateSendMessage
"""
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
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('告訴我秘密',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='這個看不到',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/wpM584d.jpg',
            title='行銷搬進大程式',
            text='選單功能－TemplateSendMessage',
            actions=[
                PostbackAction(
                    label='偷偷傳資料',
                    display_text='檯面上',
                    data='action=檯面下'
                ),
                MessageAction(
                    label='光明正大傳資料',
                    text='我就是資料'
                ),
                URIAction(
                    label='行銷搬進大程式',
                    uri='https://marketingliveincode.com/'
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
