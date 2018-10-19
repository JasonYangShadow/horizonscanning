from basecrawl import BaseCrawl
import praw
import string
import time
from datetime import date
from praw.models import MoreComments
from textprocess import *
import operator
import re

class RedditCrawl(BaseCrawl):

    def __init__(self,config_path = 'config.ini'):
        super().__init__('redditcrawl','crawling reddit website',config_path)
        self.__client_id = self.config.getValue('Reddit','CLIENT_ID')
        self.__client_secret = self.config.getValue('Reddit','CLIENT_SECRET')
        self.__redirect_url = 'http://localhost:8080'
        self.__user_agent = 'web:sip_gsdm:1 (by /u/jasonyangshadow)'
        self.__reddit = praw.Reddit(client_id = self.__client_id, client_secret = self.__client_secret, redirect_url = self.__redirect_url, user_agent = self.__user_agent)

    def request(self, params = None):
        subreddit = self.__reddit.subreddit(params['name'])
        ret = {}
        lim = 50
        if 'limit' in params:
            lim = params['limit']
        for sub in subreddit.new(limit = lim):
            key = sub.permalink
            ret[key] = {}
            ret[key]['url'] = sub.url
            ret[key]['title'] = sub.title
            ret[key]['text'] = sub.selftext.strip( '\n').replace("\n","")
            ret[key]['time'] = date.fromtimestamp(sub.created).strftime("%Y-%m-%d")
            sub.comments.replace_more(limit = None)
            ret[key]['comment_num'] = len(sub.comments.list())
            #ret[key]['comment'] = []
            #for comment in sub.comments.list():
            #    ret[key]['comment'].append(comment.body.replace('\n','').replace('\t',''))
            ret[key]['sentences'] = re.split('[\.!?]+',ret[key]['text'])
        return ret

    def resolve(self, data = None):
        t = TextProcess()
        for k,v in data.items():
            sentiment = SentimentAnalysis(v['text'])
            if (sentiment is not None and len(sentiment) > 0) and (sentiment[0] == 'neg') and (sentiment[1] > 0.7):
                print('='*50)
                print(v['text'])
                print('-'*50)
                print(t.findTopics(v['text']))
                print('-'*50)
                sentences_sentiment = {}
                for sen in v['sentences']:
                    sen = sen.strip(' \n\r\t')
                    s_tmp = SentimentAnalysis(sen)
                    if s_tmp is not None and len(s_tmp) > 0 and s_tmp[0] == 'neg':
                        sentences_sentiment[sen] = SentimentAnalysis(sen)
                sorted_by_value = sorted(sentences_sentiment.items(), key=lambda x:x[1], reverse=True)
                for key,value in sorted_by_value:
                    print('{0} => {1}'.format(key,value))
                print('-'*50)
                print("comment count: %d" % v['comment_num'])
