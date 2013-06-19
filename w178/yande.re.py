# coding: utf-8

import httplib2
from BeautifulSoup import BeautifulSoup
import argparse, json, os
import libClip
import re

#https://yande.re/data/preview/ec/46/ec462f5f8b538642ee33ec35688a578d.jpg
#https://yande.re/post/show/232622

def fixUrl(url):     
    m = re.match('\d+',url)
    if m:
        return 'https://yande.re/post/show/' + m.group()
    
    m = re.match('https://yande.re/post/show/\d+',url)
    if m:         
        return url
    return None

def getImgUrl(u):
    h = httplib2.Http('.cache')
    resp, content = h.request(u, "GET")
    soup = BeautifulSoup(content)
    a = soup.find('a',attr={'id':'highres'})
    print a['href']

def downLoad(url): 
    """   url =  https://yande.re/post/show/[id]  or id   """
    url = fixUrl(url)
    if not url:
        return
    imgurl = getImgUrl(url)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('URL', nargs='*', help='https://yande.re/post/show/[id] or id or Clip')
    results = parser.parse_args()
    urls = results.URL 
    urls.append(libClip.get())
    for u in urls:
        downLoad(u)
if __name__ == '__main__':
    main()