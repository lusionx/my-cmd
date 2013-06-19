# coding: utf-8

import httplib2, urllib
from BeautifulSoup import BeautifulSoup
import argparse, json, os

def loadDir(u):
    h = httplib2.Http()
    resp, content = h.request(u, "GET")
    #content = content.decode('gb2312')
    soup = BeautifulSoup(content,fromEncoding='GB18030')
    links = []
    for div in soup.findAll('ul', attrs={'class':'mh-directory-list'}):
        for a in div.findAll('a'):
            links.append(('http://manhua.7k7k.com' + a['href'],a.string))
    ss = ''
    for k,v in links:
        a = 'python ../bin/manhua7k7k.py -d %s %s' % (k, v)
        print a
        ss += a + '\n'
    open('index.txt','w').write(ss.encode('utf-8'))
    return links

def loadInfo(u):
    h = httplib2.Http(".cache")
    resp, content = h.request(u, "GET")
    content = content.decode('utf-8')
    soup = BeautifulSoup(content)
    title = soup.find('h1').string
    soup = soup.find('div', attrs={'class':'anim-main_list'})
    tds = soup.findAll('td')
    print u'%s by %s, states %s, last %s' % (title, tds[2].find().string, tds[4].find().string, tds[8].find().string)
    
def downImg(u):
    h = httplib2.Http()
    resp, content = h.request(u, "GET")
    content = content.decode('GB18030')
    content = content.split('\n')
    title = content[16][-7:-3]
    content = content[20].split(';')
    urls = []
    for arr in content:
        line = arr.split("'")
        if len(line) > 2:
            urls.append(line[1])
    i = 0
    domain = u'http://m.uimg.cn'
    for a in urls:
        i+=1
        f = open(title + u'_' + os.path.basename(a),'wb')
        print '%s/%s %s to %s ' % (i, len(urls), a, f.name, )
        resp, byts = h.request(domain + urllib.quote(a.encode('utf-8')), "GET")
        f.write(byts)
        f.close()
    
        
def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', action="store_true", help='load list from URL')
    group.add_argument('-i', action="store_true", help='show URL info ')
    group.add_argument('-d', action="store_true", help='down imgs from URL')
    parser.add_argument('URL', nargs=1, help='http://manhua.7k7k.com/manhua/[id].html')
    results = parser.parse_args()
    u = results.URL[0]
    if len(u) < 5 or u[:4] != u'http':
        u = 'http://manhua.7k7k.com/manhua/%s.html' % u
    if results.l :
        loadDir(u)
    if results.i:
        loadInfo(u)
    if results.d :
        downImg(results.URL[0])
if __name__ == '__main__':
    main()