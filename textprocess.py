import pycurl
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode
try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
import json
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, models
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
from exception import *

import nltk
nltk.download('wordnet')

TOPICS = 5 
NUM_WORDS = 10 

def CurlRequest(data, url = 'http://text-processing.com/api/sentiment/'):
    c = pycurl.Curl()
    buf = BytesIO()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.WRITEFUNCTION,buf.write)
    post_data = {'text':data}
    post_field = urlencode(post_data)
    c.setopt(c.POSTFIELDS,post_field)
    c.perform()
    c.close()

    res = buf.getvalue().decode('UTF-8')
    if res != None and res != "":
        d = json.loads(res)
        if 'label' in d:
            return d['label']
        else:
            return None
    else:
        return None

def SentimentAnalysis(data, url = 'http://text-processing.com/api/sentiment/'):
    c = pycurl.Curl()
    buf = BytesIO()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.WRITEFUNCTION,buf.write)
    post_data = {'text':data}
    post_field = urlencode(post_data)
    c.setopt(c.POSTFIELDS,post_field)
    c.perform()
    c.close()

    res = buf.getvalue().decode('UTF-8')
    if res != None and res != "":
        print(res)
        d = json.loads(res)
        if 'label' in d:
            return [d['label'], d['probability'][d['label']]]
        else:
            return None
    else:
        return None


class TextProcess:
    def __init__(self):
        self.__stemmer = SnowballStemmer(language = 'english')

    def lemmatizeText(self,text):
        return self.__stemmer.stem(WordNetLemmatizer().lemmatize(text))

    def preprocess(self,text):
        result = []
        #prreprocess the tweets, i.e, removing links, rt, username
        text = re.sub(r'@\w+','',text)
        text = re.sub(r'http:\/\/\w+(\.\w+)*','',text)
        #print(text)
        for token in simple_preprocess(text):
            if token not in STOPWORDS and len(token)>3:
                result.append(self.lemmatizeText(token))
        return result

    def findTopics(self,text):
        tokens = self.preprocess(text)
        if not isinstance(tokens, list):
            raise TeleException(Type.WrongTypeException,'tokens should be list')
        dictionary = corpora.Dictionary([tokens])
        corpus = [dictionary.doc2bow(tokens)]
        lda_model = models.ldamodel.LdaModel(corpus, num_topics = TOPICS, id2word = dictionary, passes = 20)
        return lda_model.print_topics(num_topics = TOPICS, num_words = NUM_WORDS)
