from basecrawl import BaseCrawl
import praw

class RedditCrawl(BaseCrawl):

    def __init__(self,config_path = 'config.ini'):
        super().__init__('redditcrawl','crawling reddit website',config_path)
        self.__client_id = self.config.getValue('Reddit','CLIENT_ID')
        self.__client_secret = self.config.getValue('Reddit','CLIENT_SECRET')
        self.__redirect_url = 'http://localhost:8080'
        self.__user_agent = 'web:sip_gsdm:1 (by /u/jasonyangshadow)'
        self.__reddit = praw.Reddit(client_id = self.__client_id, client_secret = self.__client_secret, redirect_url = self.__redirect_url, user_agent = self.__user_agent)

    def getAllSubmissions(self,name):
        subreddit = self.__reddit.subreddit(name)
        for sub in subreddit.hot(limit = 1):
            print(sub.title)
            print(sub.selftext)
            print(sub.permalink)
            print(sub.comments[0].body)
            print(sub.comments[0].list())
