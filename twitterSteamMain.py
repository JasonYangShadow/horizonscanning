from twittercrawl import TwitterCrawl

if __name__ == '__main__':
    param = {}
    param['q'] = "Japan Travel OR Japan Tourism"
    twittercrawl = TwitterCrawl('config.ini')
    twittercrawl.run(param,False)
