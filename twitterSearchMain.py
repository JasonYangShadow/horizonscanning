from twittercrawl import TwitterCrawl
import time

if __name__ == '__main__':
    param = {}
    param['q'] = "Japan Travel OR Japan Tourism"
    twittercrawl = TwitterCrawl('config.ini')
    twittercrawl.search(param)
    time.sleep(6*3600)
