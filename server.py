import string
import random
import datetime
import urllib
from flask import Flask, render_template, redirect, url_for, request, session, make_response
from mongo import Mongo
from config import Config
import json

app = Flask(__name__, static_url_path='',static_folder='templates',template_folder='templates')
app.secret_key = 'qawsedrftgyh1234567'
config = Config('config.ini')
mongo = Mongo('config.ini')

update_inteval = 20
data_inteval = 5
max_char = 50

def GenerateRadom(size = 24):
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*') for _ in range(size))

@app.route("/")
def index():
    id = GenerateRadom()
    resp = make_response(render_template('index.html'))
    resp.set_cookie('id',id)
    session[id] = datetime.datetime.now()
    return resp

@app.route("/data")
def data():
    reddit_db = config.getValue('Mongo','DB_REDDIT')
    twitter_db = config.getValue('Mongo','DB_TWITTER')
    news_db = config.getValue('Mongo','DB_NEWS')

    reddit_data = mongo.findSkipLimit(reddit_db,0,50)
    twitter_data = mongo.findSkipLimit(twitter_db,0,50)
    news_data = mongo.findSkipLimit(news_db,0,50)

    data_list = []
    if len(reddit_data) > 0:
        for d in reddit_data:
            data_item = {}
            data_item['source'] = 'reddit'
            data_item['url'] = d['url']
            data_item['time'] = d['time']
            data_item['title'] = d['title']
            if len(d['text']) > max_char:
                data_item['content'] = d['text'][:max_char].strip()
            else:
                data_item['content'] = d['text']
            data_list.append(data_item)
    if len(twitter_data) > 0:
        for d in twitter_data:
            data_item = {}
            data_item['source'] = 'twitter'
            data_item['content'] = d['content']
            data_item['title'] = d['hashtags']
            data_item['time'] = d['time']
            data_list.append(data_item)
    if len(news_data) > 0:
        print(len(news_data))
        for d in news_data:
            data_item = {}
            data_item['source'] = 'news'
            data_item['title'] = d['title']
            data_item['url'] = d['url']
            data_item['time'] = d['time']
            if len(d['description']) > max_char:
                data_item['content'] = d['description'][:max_char].strip()
            else:
                data_item['content'] = d['description']
            data_list.append(data_item)
    return json.dumps(data_list)

@app.route("/update",methods = ['POST'])
def update():
    id = request.cookies.get('id')
    if id is None:
        return redirect(url_for('index'))
    else:
        last = session[id]
        if last is None:
            return redirect(url_for('index'))
        else:
            if isinstance(last, str):
                last = datetime.datetime.strptime(last,'%Y/%m/%d %H:%M:%S')
            curr = datetime.datetime.now()
            td = curr - last
            if td.total_seconds() < update_inteval:
                return ''
            else:
                session[id] = curr
                data = {}
                data['poix0'] = '41.8625,-87.6166;ffffff;000000;20;topic is very good'
                data['poix1'] = '41.94833,-87.6555;ffffff;000000;20;C'
                data['app_id'] = 'F5lomBuB7fkRhnxcAnp0'
                data['app_code'] = 'lMT_3-fgAqE_JEb9LejqwQ'
                return "https://image.maps.api.here.com/mia/1.6/mapview?"+urllib.parse.urlencode(data)

if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = 8080,debug = False)
