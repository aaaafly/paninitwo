import random
from flask import Flask, request, abort
from imgurpython import ImgurClient

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import tempfile,os
from config import client_id, client_secret, album_id

import re
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
SECRET = os.environ.get('SECRET')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

#--------------my_function--------------#

#妮封面

client = ImgurClient(client_id, client_secret)
images = client.get_album_images('37qwmzq')
Ni_ask_URL = images[0].link
Ni_URL_1 = images[1].link
Ni_URL_2 = images[2].link
Ni_URL_3 = images[3].link
#---------------------------------------
def youtube_search(input):
    string = input

    url = "https://www.youtube.com/results?search_query=" + string
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,'html.parser')
    last = ['empty']
    i=0

    for entry in soup.select('a'):
        m = re.search("v=(.*)",entry['href'])
        if m:
            target = m.group(1)

            if target == last[i]:
                continue
            if re.search("list",target):
                continue
            last.append(target)
            i=i+1

    result = '1. https://youtu.be/'+last[1]+'\n2. https://youtu.be/'+last[2]+'\n3. https://youtu.be/'+last[3]
    return result
#---------------------------------------
def my_function(input):
    #轉小寫
    input=input.lower()
    check=input.find("youtube=")
    if(check != -1):
        output = youtube_search(input[8:])
    else:
        output='test'
    return output
#--------------my_function--------------#

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
    
    out = my_function(get)
    msg = TextSendMessage(out)

    #回復訊息msg
    line_bot_api.reply_message(event.reply_token,msg)        

if __name__ == "__main__":
    app.run()