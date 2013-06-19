# coding: utf-8

import httplib2
from BeautifulSoup import BeautifulSoup
import argparse, json, os, zipfile

domain = "http://comic.131.com"

def loadDir(u):
    h = httplib2.Http()
    resp, content = h.request(u, "GET")
    content = content.decode('utf-8')
    soup = BeautifulSoup(content)
    links = [] 
    for div in soup.findAll('ul', attrs={'class':'mh_fj'}):
        for a in div.findAll('a'):
            if a['href'][:len(domain)] == domain:                
                links.insert(0,(a['href'],a.contents[0]))
            else :
                links.insert(0,(domain + a['href'],a.contents[0]))
    ss = ''
    for k,v in links:
        a = 'mh131 -d %s %s' % (k,v)
        print a
        ss += a + '\n'
    open('index.txt','w').write(ss.encode('utf-8'))
    return links

def loadInfo(u):
    pass

def downImg(u):
    root = u.split('/')[:-1]
    root = '/'.join(root) + '/%s.html'
    #找出一共多少页
    h = httplib2.Http()
    resp, content = h.request(u, "GET")
    content = content.decode('utf-8')
    soup = BeautifulSoup(content)
    title = soup.find('div', attrs={'class':'mh_szwz2'})
    title = title.findAll('a')[-1].string
    #print title
    pages = []
    #生成所有的page地址 http://comic.131.com/content/15159/156936/[xx].html
    for a in soup.find('select', attrs={'id':'jumpMenu'}).findAll('option'):
        #print a['value']
        pages.append(root % a['value'])
    files = []
    i = 1
    for url in pages:
        resp, content = h.request(url, "GET")
        content = content.decode('utf-8')
        soup = BeautifulSoup(content)
        img = soup.find('img', attrs={'id':'comicBigPic'})['src']
        #img = imgjs.split('?img=')[1]
        resp, bytes = h.request(img, "GET")
        fileName = '%s_%03d%s' % (title, i, os.path.splitext(img)[1])
        print '%3d/%s from %s to %s' % (i, len(pages), img, fileName)
        f = open(fileName,'wb')
        f.write(bytes)
        f.close()
        files.append(fileName)
        i+=1
    zipImgs(title, files)

def zipImgs(name,files):
    zf = zipfile.ZipFile(name + '.zip', 'w')
    for a in files:
        zf.write(a)
        os.remove(a)
    zf.close()

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', action="store_true", help='load list from URL')
    group.add_argument('-i', action="store_true", help='show URL info ')
    group.add_argument('-d', action="store_true", help='down imgs from URL')
    parser.add_argument('URL', nargs=1, help='[http://manhua.178.com/]<xxxx> | URL')
    results = parser.parse_args()
    if results.l :
        loadDir(results.URL[0])
    if results.i:
        loadInfo(results.URL[0])
    if results.d :
        downImg(results.URL[0])
if __name__ == '__main__':
    main()