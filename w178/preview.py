# coding: utf-8

import httplib2, json
from BeautifulSoup import BeautifulSoup
import os, argparse

def gfeed(u):
    h = httplib2.Http()
    """http://www.google.com/uds/Gfeeds?num=50&q=https%3A%2F%2Fyande.re%2Fpost%2Fatom&scoring=h&v=1.0"""
    url = 'https://ajax.googleapis.com/ajax/services/feed/load?'
    url += 'v=1.0&num=100&output=json&scoring=h&q='
    url += u
    resp, content = h.request(url, "GET")
    content = json.loads(content)['responseData']['feed']['entries']
    return content

def loadAotm(u):
    entries = gfeed(u)
    for entry in entries: 
        id = entry['link']
        id = id[id.rfind('/') + 1:]
        if os.path.isfile(id + '.jpg'):
            continue
        else:
            soup = BeautifulSoup(entry['content'])
            view = soup.find('img')['src']
            cmd = 'curl -k -o %s.jpg %s' % (id, view)
            os.system(cmd)

def downImg(id):
    cmd = 'curl -k -o d.htm https://yande.re/post/show/' + id
    os.system(cmd)
    soup = BeautifulSoup(open('d.htm').read())
    src = soup.find('img',attrs = {'id':'image'})['src']
    #print src
    cmd = 'curl -k -o 00/%s.jpg "%s"' % (id, src)
    os.system(cmd)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', action="store_true", help='load atom')
    parser.add_argument('-d', help='down img id')
    results = parser.parse_args() 
    if results.l :
        loadAotm('https://yande.re/post/atom')
    if results.d :
        downImg(results.d)

if __name__ == '__main__':
    main()