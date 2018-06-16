import unittest
from pprint import pprint
from newscrawl import NewsCrawl

class TestCrawl(unittest.TestCase):

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
