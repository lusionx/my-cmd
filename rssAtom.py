# -*- coding: utf-8 -*-
#!/usr/bin/python

"""通过google feed api取得rss
http://code.google.com/apis/feed/v1/jsondevguide.html#resultBasic
"""

import urllib, httplib2
import json


def load(url):
    h = httplib2.Http('.cache')
    data = {}
    data['q'] = url
    data['v'] = '1.0'
    #data['output'] = 'xml'
    data['num'] = -1
    url = 'https://ajax.googleapis.com/ajax/services/feed/load?'
    url += urllib.urlencode(data)
    print url
    resp, content = h.request(url, "GET")
    return json.loads(content)['responseData']['feed']
    
def main(arg):
    feed = load(arg)
    print feed['entries'][0]['content'].encode('utf-8')

if __name__ == '__main__':
    urls = []
    urls.append('http://bt.ktxp.com/rss-sort-1.xml')
    main(urls[0])
    raw_input()

