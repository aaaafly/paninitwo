
#----------------import----------------------#
import os
from myID import *

#----------------line bot api----------------#
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)
#----------------ACCESS_TOKEN----------------#
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
SECRET = os.environ.get('SECRET')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)
#----------------ACCESS_TOKEN----------------#

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


@handler.add(MessageEvent, message=(ImageMessage, TextMessage))
def handle_message(event):
    #get取的訊息
    get = event.message.text
#------------------------------------------------------------------------------------------------------#
    if(get == 'test'):
        print(event.source)
        msg = TextSendMessage('ok')
        #回復訊息msg
        line_bot_api.reply_message(event.reply_token,msg)        
# -----------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    app.run()