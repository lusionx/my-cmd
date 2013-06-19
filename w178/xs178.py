# coding: utf-8

import httplib2
from BeautifulSoup import BeautifulSoup
import argparse, json, os

def downTxt(u):
    h = httplib2.Http()
    resp, content = h.request(u, "GET")
    content = content.decode('utf-8')
    lines = [ a.rstrip() for a in content.split('\n')]
    id = [line for line in lines if line[:18]=='var g_lnovel_id = '][0][19:-2]
    title = [line for line in lines if line[:20]=='var g_lnovel_name = '][0][21:-2] + '['
    soup = BeautifulSoup(content)
    links = []  #http://xs.178.com/460/1732/1732.txt
    for a in soup.findAll('a',attrs={'class':'download_href'}):
        t = title + a.parent.nextSibling.string.strip() + u'].txt'
        t = t.replace('/','_')
        t = t.replace('\\','_')
        links.append(( u'http://xs.178.com/%s/%s/%s.txt' % (id,a['id'],a['id']), t))
    #print links[0][0]
    #print links[0][1]
    
    h = httplib2.Http()
    for u, n in links:
        print 'Download %s from %s' % (n, u)
        f = open(n,'w')
        resp, content = h.request(u, "GET")
        content = content.decode('utf-8')
        f.write(content.encode('utf-8'))
        f.close()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('id', type=int, nargs=1, help='178 url')
    result = parser.parse_args()
    if result.id:
        #print result.id[0]
        u = u'http://xs.178.com/'+str(result.id[0])+u'/index.shtml'
        print 'Load ' + u
        downTxt(u)