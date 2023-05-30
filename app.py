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

#姜
import pygsheets
import pandas as pd
import numpy as np
import random
gc = pygsheets.authorize(service_file='./google_python.json')
sht = gc.open_by_url(
'https://docs.google.com/spreadsheets/d/1vgEdIDyq72ond0Tch48kNiJ7N_0FmN04dB38bErMLQg/edit?hl=zh-TW#gid=0'
)
wks_list = sht.worksheets()
wks = sht[0]
#讀取成 df
df = pd.DataFrame(wks.get_all_records())
column_names = df.columns
# 隨機打亂表格的順序，讓每次隨機都不一樣
#df_shuffled = df.sample(frac=1)  
###################################################

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('5kd4nm3bDWl+WVCow3m0qje706VXFDrsSgB0QiB/ZOB2ZFIj5mXMYm6U6AAdh31+yIOY+sdNl9blhd0qijZl9lB7+W5l7jNZ+kOWbYG8tYDUY3MBk2nMu5nNN1XdfFY7VeAowBCB/GpOmhX8VganBAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
parser = WebhookParser('1441b0c3a47a16b4205287848d9daa91')

# push message
#line_bot_api.push_message('U26e6062efb6aacd3b61e235ce67a0587', TextSendMessage(text='輸入「吃什麼好呢」以啟動篩選店家功能 ; 輸入「自動推薦」隨機推薦您三家店家'))

rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=1200, height=405),
    selected=True, #當使用者加入linebot或重設linebot時，會顯示這個 Rich Menu
    name='快點啦', 
    chat_bar_text='Tap here', #設定 Rich Menu 上方的聊天視窗顯示的文字，這裡設定為 "Tap here"。
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=600, height=405),
            action=MessageAction(text='按鈕1')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=600, y=0, width=600, height=405),
            action=MessageAction(text='按鈕2')
        )
    ]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create) #建立rich menu並取得rich menu的id

# 將 Rich Menu 指派給預設使用者（所有使用者在與此 Line Bot互動時都會看到並使用該 Rich Menu）
line_bot_api.set_default_rich_menu(rich_menu_id)

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
        if isinstance(event,PostbackEvent):
            if event.postback.data[0:1] == 'Z':
                df_shuffled = df.sample(frac=1),
                random_output = df_shuffled.iloc[:3] # 直接选择前三行
                random_output['餐廳名稱'] = random_output['類型'] + random_output['餐廳']
                output = random_output[['餐廳名稱','店名','地址','連結']]
                output = output.applymap(str.strip)  # 去除每个字段的额外空格
                o_string = output.to_string(index=False, header=False)
                output_lines = [line.strip() for line in o_string.split('\n')]
                output_string = '\n'.join(output_lines)
                line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=output_string)
                    )
            
            elif event.postback.data[0:1] == 'X':
                area=event.postbackdata[2:]
                line_bot_api.reply_message(   # 回復「選擇價位類別」按鈕樣板訊息
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
                                    data='A&餐廳'+'&'+ area
                                ),
                                PostbackTemplateAction(
                                    label='飲料店',
                                    text='飲料店',
                                    data='B&飲料店'+'&'+ area
                                ),
                                PostbackTemplateAction(
                                    label='咖啡廳',
                                    text='咖啡廳',
                                    data='B&咖啡廳'+'&'+ area
                                ),
                                PostbackTemplateAction(
                                    label='酒吧',
                                    text='酒吧',
                                    data='B&酒吧'+'&'+ area
                                )
                            ]
                        )
                    )
                )
            elif event.postback.data[0:1] == 'A':
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
                                    data='C&' + restaurant + '&$'
                                ),
                                PostbackTemplateAction(
                                    label='$150-$300',
                                    text='中價位',
                                    data='C&' + restaurant + '&$$'
                                ),
                                PostbackTemplateAction(
                                    label='$300以上',
                                    text='高價位',
                                    data='C&' + restaurant + '&$$$'
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
                                    data='D&' + shoptype + '&4'
                                ),
                                PostbackTemplateAction(
                                    label='4.5星以上',
                                    text='真嚴格',
                                    data='D&' + shoptype + '&4.5'
                                ),
                                PostbackTemplateAction(
                                    label='隨機',
                                    text='都行',
                                    data='D&' + shoptype + '&0'
                                )
                            ]
                        )
                    )
                )
            elif event.postback.data[0:1] == "C":
                if '早午餐' in event.postback.data:
                    restaurant = event.postback.data[2:5]
                    pricechoice = event.postback.data[6:]
                else:
                    restaurant = event.postback.data[2:4]
                    pricechoice = event.postback.data[5:]
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
                                    data='E&' + restaurant + '&' + pricechoice + '&4'
                                ),
                                PostbackTemplateAction(
                                    label='4.5星以上',
                                    text='真嚴格',
                                    data='E&' + restaurant + '&' + pricechoice + '&4.5'
                                ),
                                PostbackTemplateAction(
                                    label='隨機',
                                    text='都行',
                                    data='E&' + restaurant + '&' + pricechoice + '&0'
                                )
                            ]
                        )
                    )
                )
            elif event.postback.data[0:1] == "E":
                result = event.postback.data.split('&')
                df_shuffled = df.sample(frac=1)
                select=df_shuffled['類型']==result[1]
                select1 = pd.to_numeric(df_shuffled['評價'], errors='coerce') >= float(result[3])
                select2=df_shuffled['價位']==result[2]
                selected_rows = df_shuffled[select & select1& select2]
                if len(selected_rows) >= 5:
                    random_selection = random.sample(selected_rows.index.tolist(),5)
                    random_output= selected_rows.loc[random_selection]
                    output = random_output[['店名','地址', '連結']]
                    output = output.applymap(str.strip)  # 去除每个字段的额外空格
                    o_string = output.to_string(index=False, header=False)
                    output_lines = [line.strip() for line in o_string.split('\n')]
                    output_string = '\n'.join(output_lines)
        
                elif len(selected_rows)==0:
                    output_string="附近沒有店家符合此條件～～請再試一次"
        
                else:
                    random_output = selected_rows
                    output = random_output[['店名','地址', '連結']]
                    output = output.applymap(str.strip)  # 去除每个字段的额外空格
                    o_string = output.to_string(index=False, header=False)
                    output_lines = [line.strip() for line in o_string.split('\n')]
                    output_string = '\n'.join(output_lines)
                line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=output_string)
                    )
            elif event.postback.data[0:1] == "D":
                result = event.postback.data.split('&')
                df_shuffled = df.sample(frac=1)
                select=df_shuffled['類型']==result[1]
                select1 = pd.to_numeric(df_shuffled['評價'], errors='coerce') >= float(result[2])
                selected_rows = df_shuffled[select & select1]
                
                if len(selected_rows) >= 5:
                    random_selection = random.sample(selected_rows.index.tolist(), 5)
                    random_output = selected_rows.loc[random_selection]
                    output = random_output[['店名','地址', '連結']]
                    output = output.applymap(str.strip)  # 去除每个字段的额外空格
                    o_string = output.to_string(index=False, header=False)
                    output_lines = [line.strip() for line in o_string.split('\n')]
                    output_string = '\n'.join(output_lines)
                    
                elif len(selected_rows)==0:
                    output_string="附近沒有店家符合此條件～～請再試一次"

                else:
                    random_output = selected_rows
                    output = random_output[['店名','地址', '連結']]
                    output = output.applymap(str.strip)  # 去除每个字段的额外空格
                    o_string = output.to_string(index=False, header=False)
                    output_lines = [line.strip() for line in o_string.split('\n')]
                    output_string = '\n'.join(output_lines)
                line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        # 爬取該地區正在營業，且符合所選擇的美食類別的前五大最高人氣餐廳
                        TextSendMessage(text=output_string)
                    )
                
    return 'ok'
    #else:
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)