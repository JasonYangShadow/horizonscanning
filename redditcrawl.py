from basecrawl import BaseCrawl
import praw
import string
import time
from datetime import date
from praw.models import MoreComments
from textprocess import *

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
            ret[key]['sentences'] = ret[key]['text'].split('.')
        return ret

    def resolve(self, data = None):
        for k,v in data.items():
            sentiment = SentimentAnalysis(v['text'])
            if (len(sentiment) > 0) and (sentiment[0] == 'neg') and (sentiment[1] > 0.7):
                print(v['text'])
                t = TextProcess()
                print(t.findTopics(v['text']))
                sentences_sentiment = {} 
                for sen in v['sentences']:
                    s_tmp = SentimentAnalysis(sen)
                    if s_tmp[0] == 'neg':
                        sentences_sentiment[sen] = SentimentAnalysis(sen)
                print(sentences_sentiment)
                print(v['comment_num'])
