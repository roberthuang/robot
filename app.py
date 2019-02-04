from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('X6HvDoq3VZFWZgOeyLKEShvaK36uQE0Sg+BE45L/sYR06SbYIiTuX33N/xTVP0xxcVlgYkUscTKvBV2W7gaI4gyTS/WRQsZp28GYggewsfGjK81IH7O41Xv7Si1Sl70qEVpBsC61C6RRQeeBjlp7AQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('b24033d9c9bff1aa900283ef483f04c4')

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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text=event.message.text

    if (text=="Hi"):
        reply_text = "Hello"
    elif(text=="你好"):
        reply_text = "哈囉"
    elif(text=="機器人"):
        reply_text = "叫我嗎"
    else:
        reply_text = text

    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
