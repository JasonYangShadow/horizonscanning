import unittest
from pprint import pprint
from newscrawl import NewsCrawl
from twittercrawl import TwitterCrawl

class Test(unittest.TestCase):

    def testTwitterSearch(self):
        param = {}
        param['q'] = 'linux'
        twittercrawl = TwitterCrawl('config.ini')
        twittercrawl.search(param)

    @unittest.skip('skip')
    def testTwitter(self):
        param = {}
        param['q'] = 'public policy'
        twittercrawl = TwitterCrawl('config.ini')
        twittercrawl.run(param,False)

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

if __name__ == '__main__':
    unittest.main()
