# coding: utf-8

import httplib2
from BeautifulSoup import BeautifulSoup
import argparse, json, os, zipfile

def loadDir(u):
    h = httplib2.Http()
    resp, content = h.request(u, "GET")
    content = content.decode('utf-8')
    soup = BeautifulSoup(content)
    links = []
    for div in soup.findAll('div', attrs={'class':'cartoon_online_border'}):
        for a in div.findAll('a'):
            links.append((a['href'],a.string))
    #links = sorted(links,key = lambda x:x[1].replace(u'第',''))
    ss = ''
    for k,v in links:
        if k[:4] != 'http':
            k = 'http://www.dmzj.com' + k
        a = 'mh178 -d %s %s' % (k,v)
        print a
        ss += a + '\n'
    open('index.txt','w').write(ss.encode('utf-8'))
    return links

def loadInfo(u):
    h = httplib2.Http()
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
    content = content.decode('utf-8')
    content = content.split('\n')
    ss = [line for line in content if line[:26]=='eval(function(p,a,c,k,e,d)'][0]
    f = open('tmp.js','w')
    f.write(ss+';console.log(pages);')
    f.close()
    ss = os.popen('node tmp.js').readlines()[0]
    ss = json.loads(ss)
    #print ss
    #return;
    title = [line for line in content if line[:21]=='var g_chapter_name = '][0][22:-2]
    
    domain = u'http://imgfast.dmzj.com/'
    i = 0
    svPaths = []
    for a in ss:
        i += 1
        f = open(title + u'_' + '%03d%s' % (i, os.path.splitext(a)[1]), 'wb')
        svPaths.append(f.name)
        print '%3d/%s %s to %s ' % (i, len(ss), domain + a, f.name, )
        resp, byts = h.request(domain + a.replace(' ','%20'), "GET")
        #print resp
        f.write(byts)
        f.close()
    #title = title.lstrip(u'第')
    zf = zipfile.ZipFile(title + '.zip', 'w')
    for a in svPaths:
        zf.write(a)
        os.remove(a)
    zf.close()
    
def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', action="store_true", help='load list from URL')
    group.add_argument('-i', action="store_true", help='show URL info ')
    group.add_argument('-d', action="store_true", help='down imgs from URL')
    parser.add_argument('URL', nargs=1, help='[http://www.dmzj.com/]<xxxx> | URL')
    results = parser.parse_args()
    u = results.URL[0]
    if len(u) < 5 or u[:4] != u'http':
        u = 'http://www.dmzj.com/' + u
    if results.l :
        loadDir(u)
    if results.i:
        loadInfo(u)
    if results.d :
        downImg(results.URL[0])
if __name__ == '__main__':
    main()