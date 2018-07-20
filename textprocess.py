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

