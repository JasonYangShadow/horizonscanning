from twython import Twython, TwythonStreamer
from basecrawl import BaseCrawl
from pprint import pprint
from mongo import Mongo

class CustomStreamer(TwythonStreamer):
    def __init__(self, api_key, api_secret, access_key, access_secret, queue):
        super().__init__(app_key = api_key, app_secret = api_secret, oauth_token = access_key, oauth_token_secret = access_secret)
        self.__queue = queue

    def on_success(self,data):
        do = {}
        if 'retweeted_status' in data:
            return
        if 'quoted_status' in data:
            return
        if data['lang'] != 'en':
            return
        if data['place'] is None:
            return
        do['hashtags'] = []
        if data['truncated'] == False:
            do['text'] = data['text']
            for d in data['entities']['hashtags']:
                do['hashtags'].append(d['text'])
        else:
            do['text'] = data['extended_tweet']['full_text']
            for d in data['extended_tweet']['entities']['hashtags']:
                do['hashtags'].append(d['text'])
        do['user'] = {}
        do['user']['id'] = data['user']['id']
        do['user']['id_str'] = data['user']['id_str']
        do['user']['name'] = data['user']['screen_name']
        do['user']['location'] = data['user']['location']

        do['place'] = data['place']

        if self.__queue.full():
            raise TeleException(Type.FullException,'queue is full')
        else:
            self.__queue.put(do)

    def on_error(self, status_code, data):
        print(status_code)

class TwitterCrawl(BaseCrawl):
    def __init__(self, config_path = 'config.ini'):
        super().__init__('twittercrawl','crawling twitter website',config_path)
        self.__api_key = self.config.getValue('Twitter','API_KEY')
        self.__api_secret = self.config.getValue('Twitter','API_SECRET')
        self.__access_key = self.config.getValue('Twitter','ACCESS_KEY')
        self.__access_secret = self.config.getValue('Twitter','ACCESS_SECRET')

    def request(self, param = None):
        stream = CustomStreamer(self.__api_key, self.__api_secret, self.__access_key, self.__access_secret, self.queue)
        if 'q' not in param:
            raise TeleException(Type.NoneException,'you should at least put q inside param')
        stream.statuses.filter(track = param['q'], language='en')

    def resolve(self, data = None):
        mdata = []
        mdata.append(data)
        mongo = Mongo('config.ini')
        mongo.insert(mdata,'stream_tweets')
        pprint(data)

    def search(self,param):
        if param == None:
            raise TeleException(Type.NoneException,'param should not be none')
        self.__twitter = Twython(app_key = self.__api_key, app_secret = self.__api_secret, oauth_token = self.__access_key, oauth_token_secret = self.__access_secret)
        if 'q' not in param:
            raise TeleException(Type.NoneException,'for search function, q must be set')
        count = 2000
        if 'count' in param:
            count = param['count']
        search = self.__twitter.search(q=param['q'], count=count)
        tweets = search['statuses']
        for tweet in tweets:
            print('lang is:{}, content is:{},location is:{}'.format(tweet['lang'],tweet['text'],tweet['user']['location']))
