from newsapi import NewsApiClient
from config import Config
from basecrawl import BaseCrawl
from exception import Type, TeleException
from datetime import datetime, timedelta
from pprint import pprint
from mongo import Mongo

class NewsCrawl(BaseCrawl):
    def __init__(self, config_path = 'config.ini'):
        super().__init__('newscrawl','crawling newsapi.org website',config_path)
        self.__key = self.config.getValue('newsorg','key')
        if self.__key is None:
            raise TeleException(Type.NoneException,'news api key not found')
        self.__api = NewsApiClient(api_key = self.__key)
        self.__db_file = self.config.getValue('newsorg','db_file')

    def request(self, params = None):
        if not isinstance(params, dict):
            raise TeleException(Type.WrongTypeException, 'param is not dict')
        lang = None
        if 'lang' in params:
            lang = params['lang']
        query = None 
        if 'q' in params:
            query = params['q']
        date_from = None
        if 'from' in params:
            date_from = params['from']
        else:
            yesterday = datetime.now() - timedelta(days = 1)
            date_from = yesterday.strftime('%Y-%m-%d')
        source = None
        if 'sources' in params:
            sources = params['sources']

        articles = self.__api.get_everything(q = query, language = lang, sources = sources, from_param = date_from)
        if articles['status'] == 'ok':
            return articles['articles']
        else:
            raise TeleException(Type.UnknownException, 'errcode:{0},msg:{1}'.format(articles['code'],articles['message']))

    def resolve(self, data = None):
        #mongo = Mongo()
        if not isinstance(data, list):
            raise TeleException(Type.WrongTypeException, 'data is not list')
        for d in data:
            pprint(d)
            #mongo.saveUpdateOne({'url':d['url'],{'$set':{'source':d['source']['name'],
            #    'author': d['author'], 'title': d['title'], 'description':
            #    d['description'], 'time': d['publishedAt']}}, self.__db_file)
    def getsource(self, lang = None):
        sources = self.__api.get_sources()['sources']
        source_results = []
        for source in sources:
            if lang is None or source['language'] != lang:
                continue
            source_dict = {}
            source_dict['id'] = source['id']
            source_dict['lang'] = source['language']
            source_dict['country'] = source['country'] 
            source_dict['category'] = source['category']
            source_results.append(source_dict)
        return source_results
