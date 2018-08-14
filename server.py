import string
import random
import datetime
import urllib
from flask import Flask, render_template, redirect, url_for, request, session, make_response
app = Flask(__name__)
app.secret_key = 'qawsedrftgyh1234567'

def GenerateRadom(size = 24):
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*') for _ in range(size))

@app.route("/")
def index():
    id = GenerateRadom()
    resp = make_response(render_template('index.html'))
    resp.set_cookie('id',id)
    session[id] = datetime.datetime.now()
    return resp

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
            if td.total_seconds() < 20:
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
    app.run(host = '0.0.0.0',debug = True)
