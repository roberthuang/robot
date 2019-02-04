from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import json
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
    answer = get_answer(event.message.text)

    message = TextSendMessage(text=answer)
    line_bot_api.reply_message(event.reply_token, message)


def get_answer(message_text):
    url = "https://americandrama.azurewebsites.net/qnamaker/knowledgebases/1d8c9b09-00e3-432b-9ee0-18625e1ffd17/generateAnswer"

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




import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
