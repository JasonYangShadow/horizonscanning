from twython import Twython, TwythonStreamer
from basecrawl import BaseCrawl
from pprint import pprint

class CustomStreamer(TwythonStreamer):
    def __init__(self, api_key, api_secret, access_key, access_secret, queue):
        super().__init__(app_key = api_key, app_secret = api_secret, oauth_token = access_key, oauth_token_secret = access_secret)
        self.__queue = queue

    def on_success(self,data):
        if 'text' in data:
            #pprint(data['text'])
            if self.__queue.full():
                raise TeleException(Type.FullException,'queue is full')
            else:
                pprint(data['text'])
                self.__queue.put(data['text'])

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
        stream.statuses.filter(track = param['q'])

    def resolve(self, data = None):
        pprint(data)
