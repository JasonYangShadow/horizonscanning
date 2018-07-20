import unittest
from pprint import pprint
from newscrawl import NewsCrawl
from twittercrawl import TwitterCrawl
from crypto import Crypto
from textprocess import CurlRequest

class Test(unittest.TestCase):

    @unittest.skip('skip')
    def testTwitterSearch(self):
        param = {}
        param['q'] = 'linux'
        twittercrawl = TwitterCrawl('config.ini')
        twittercrawl.search(param)

    @unittest.skip('skip')
    def testTwitter(self):
        param = {}
        param['q'] = 'tokyo'
        twittercrawl = TwitterCrawl('config.ini')
        twittercrawl.run(param,False)

    #@unittest.skip('skip')
    def testCurl(self):
        pprint(CurlRequest('i hate tokyo'))


    @unittest.skip('skip')
    def testNewsorg(self):
        param = {}
        param['lang'] = 'en'
        newcrawl = NewsCrawl('config.ini')
        source = newcrawl.getsource('en')
        if len(source) > 0:
            source_str = ','.join(list(map(lambda s: s['id'],source)))
            param['sources'] = source_str
        param['q'] = 'policy OR bitcoin OR health OR city'
        newcrawl.run(param)

    @unittest.skip('skip')
    def testencryption(self):
        crypto = Crypto()
        print(">>>")
        print(crypto.encrypt('test'))
        print("<<<")

if __name__ == '__main__':
    unittest.main()
