import unittest
from pprint import pprint
from newscrawl import NewsCrawl
from twittercrawl import TwitterCrawl
from crypto import Crypto
from textprocess import * 
from geo import *
from redditcrawl import RedditCrawl

class Test(unittest.TestCase):

    #@unittest.skip('skip')
    def testTwitterSearch(self):
        param = {}
        param['q'] = 'Japan'
        twittercrawl = TwitterCrawl('config.ini')
        twittercrawl.search(param)

    @unittest.skip('skip')
    def testGeo(self):
        pprint(GetLongLatFromName("Tokyo")) 
        pprint(GetAddressFromLongLat(34.69,139.40))


    @unittest.skip('skip')
    def testTwitter(self):
        param = {}
        param['q'] = 'travel'
        twittercrawl = TwitterCrawl('config.ini')
        twittercrawl.run(param,False)

    @unittest.skip('skip')
    def testReddit(self):
        reddit = RedditCrawl('config.ini')
        param = {}
        param['limit'] = 1000
        param['name'] = 'JapanTravel'
        reddit.run(param)

    @unittest.skip('skip')
    def testCurl(self):
        pprint(CurlRequest('though i think Tokyo is a good city to live, the expensive price of stuff turn me down'))

    @unittest.skip('skip')
    def testNewsorg(self):
        param = {}
        param['lang'] = 'en'
        newcrawl = NewsCrawl('config.ini')
        source = newcrawl.getsource('en')
        if len(source) > 0:
            source_str = ','.join(list(map(lambda s: s['id'],source)))
            param['sources'] = source_str
        param['q'] = 'Japan Tourism OR Japan Travel OR Japan'
        param['from'] = '2018-09-23'
        newcrawl.run(param)

    @unittest.skip('skip')
    def testencryption(self):
        crypto = Crypto()
        print(">>>")
        print(crypto.encrypt('test'))
        print("<<<")

    @unittest.skip('skip')
    def testTopics(self):
        t = TextProcess()
        pprint(t.findTopics("Seems like the Department of Justice (and FBI) had a program to keep Donald Trump from becoming President. @DarrellIssa  @foxandfriends  If this had happened to the other side, everybody involved would be in jail. This is a Media coverup of the biggest story of our time."))

if __name__ == '__main__':
    unittest.main()
