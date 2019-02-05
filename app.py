from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from bs4 import BeautifulSoup

import requests
import json
import random


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('X6HvDoq3VZFWZgOeyLKEShvaK36uQE0Sg+BE45L/sYR06SbYIiTuX33N/xTVP0xxcVlgYkUscTKvBV2W7gaI4gyTS/WRQsZp28GYggewsfGjK81IH7O41Xv7Si1Sl70qEVpBsC61C6RRQeeBjlp7AQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('b24033d9c9bff1aa900283ef483f04c4')

def movie():
    target_url = 'https://movies.yahoo.com.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('div.movielist_info h2 a')):
        if index == 20:
            return content
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

def apple_news():
    target_url = 'https://tw.appledaily.com/new/realtime'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 5:
            return content
        link = data['href']
        content += '{}\n\n'.format(link)
    return content

def technews():
    target_url = 'https://technews.tw/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('article div h1.entry-title a')):
        if index == 12:
            return content
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content

def panx():
    target_url = 'https://panx.asia/'
    print('Start parsing ptt hot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('div.container div.row div.desc_wrap h2 a'):
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content

def oil_price():
    target_url = 'https://gas.goodlife.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.select('#main')[0].text.replace('\n', '').split('(')[0]
    gas_price = soup.select('#gas-price')[0].text.replace('\n\n\n', '').replace(' ', '')
    cpc1 = soup.select('#cpc')[0].text.replace(' ', '')
    cpc2 = soup.select('#cpc')[1].text.replace(' ', '')
    content = '{}\n{}{}{}'.format(title, gas_price, cpc1, cpc2)

    return content

def get_answer(message_text):
    url = "https://robertbotman.azurewebsites.net/qnamaker/knowledgebases/1d8c9b09-00e3-432b-9ee0-18625e1ffd17/generateAnswer"

    # 發送request到QnAMaker Endpoint要答案
    response = requests.post(
        url,
        json.dumps({'question': message_text}),
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'EndpointKey 5f61f834-ddcd-474d-835a-623bb4602a9f'
        }
    )

    data = response.json()

    try:
        # 我們使用免費service可能會超過限制（一秒可以發的request數）
        if "error" in data:
            return data["error"]["message"]
        # 這裡我們預設取第一個答案
        answer = data['answers'][0]['answer']

        return answer

    except Exception:

        return "Error occurs when finding answer"


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

# 處理貼圖
@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
    print("[user]package_id:", event.message.package_id)
    print("[user]sticker_id:", event.message.sticker_id)
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=sticker_id
    )
    line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "蘋果即時新聞":
        content = apple_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "科技新報":
        content = technews()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "PanX泛科技":
        content = panx()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "油價":
        content = oil_price()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0



    answer = get_answer(event.message.text)

    if answer == "新聞":
        buttons_template = TemplateSendMessage(
            alt_text='新聞 template',
            template=ButtonsTemplate(
                title='新聞類型',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
                actions=[
                    MessageTemplateAction(
                        label='蘋果即時新聞',
                        text='蘋果即時新聞'
                    ),
                    MessageTemplateAction(
                        label='科技新報',
                        text='科技新報'
                    ),
                    MessageTemplateAction(
                        label='PanX泛科技',
                        text='PanX泛科技'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0

    if answer == "油價":
        content = oil_price()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if answer == "電影":
        content = movie()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)