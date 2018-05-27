import unittest
from newscrawl import NewsCrawl

class TestNews(unittest.TestCase):

    def testSearch(self):
        param = {}
        param['lang'] = 'en'
        param['sources'] = 'bbc-news, the-verge'
        newcrawl = NewsCrawl('config.ini')
        newcrawl.run(param)

if __name__ == '__main__':
    unittest.main()
