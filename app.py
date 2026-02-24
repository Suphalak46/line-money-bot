from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
import re

app = Flask(__name__)

# 🔴 ใส่ค่าของคุณตรงนี้ (จาก LINE Messaging API)
CHANNEL_ACCESS_TOKEN = "JSogIC9spvzQFeNxA9yWk7q/1+u24Qku/s7UOHFkp3W0o8pJjnQc6xzxuZkXnPS2T82W9MZ7RGGb9IY2OZpd7l28qivBy6nwyvizr3r5bhBtoGxHn6O/TTH2Jk/qDqayeYXGpuHegDCQX9444AgfmgdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "9a02eb0df9177dca61d48812c1bf4974"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()

    # ตรวจจับรูปแบบ:
    # รายรับ 500
    # รายจ่าย 200
    match = re.match(r"(รายรับ|รายจ่าย)\s+(\d+)", text)

    if match:
        type_text = match.group(1)
        amount = match.group(2)

        reply = f"บันทึกแล้ว ✅\nประเภท: {type_text}\nจำนวนเงิน: {amount} บาท"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="พิมพ์แบบนี้นะ:\nรายรับ 500\nหรือ\nรายจ่าย 200"
            )
        )


if __name__ == "__main__":
    app.run(port=5000)