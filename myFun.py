import requests
from bs4 import BeautifulSoup as bs
import json
import matplotlib.pyplot as plt
import datetime

from imgurpython import ImgurClient
import os
from myID import *




def picture():
    client = ImgurClient(client_id, client_secret)
    images = client.get_album_images(album_id_0)            
    pic_url = images[0].link
    return pic_url

def upload_photo(path):
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    config = {'album': album_id_0 }

    print("Uploading image... ")
    image = client.upload_from_path(path, config=config, anon=False)
    print("Done")

    return image['link']

def feePlot():
    apikey = 'AIzaSyAzpWOZ2DM5t84gHbBdUttvKNuuhflOJ6E'
    getvalueurl = 'https://sheets.googleapis.com/v4/spreadsheets/143RmfNG-gamYarH1e9NMfD9mmiR3h5UR0ypn4S3xtUQ/values/A2:D?key=%s' % (apikey)
    res = requests.get(getvalueurl)
    data = res.content
    jsondata = json.loads(data)
    values = jsondata['values']

    x=[]
    x_label=[]
    x1 = []
    x2 = []
    x3 = []
    y1 = []
    y2 = []
    y3 = []

    for t,y,m,fee in values:
        time = datetime.datetime(int(y),int(m),1)
        time = (time-datetime.datetime(1970,1,1)).total_seconds()
        if m not in x:
            x.append(time)
            x_label.append('{:}\n{:}'.format(y,m))
        if t == 'Water':
            y1.append(int(fee))
            x1.append(int(time))
        elif t == 'Gas':
            y2.append(int(fee))
            x2.append(int(time))
        elif t == 'Electicity':
            y3.append(int(fee))
            x3.append(int(time))

    plt.plot(x1, y1, '-o', label='Water')
    plt.plot(x2, y2, '-o', label='Gas')
    plt.plot(x3, y3, '-o', label='Electicity')

    axes = plt.subplot(111)
    axes.set_xticks(x)
    axes.set_xticklabels(x_label)
    plt.legend()

    plt.savefig('send.png')
    upload_photo('send.png')

    if os.path.exists("send.png"):
        os.remove("send.png")
    else:
        print("The file does not exist")
    return picture()