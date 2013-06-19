# coding: utf-8

import httplib2, bencode
import argparse, os
import libClip


root = os.getcwd()#os.path.dirname(__file__)

def gclip():
    return libClip.get()
    
def download(url):
    if url.split('.')[-1] != 'torrent':
        print 'wrong url ' + url
        return
    h = httplib2.Http()
    print 'down '+url
    resp, bytes = h.request(url, "GET")
    torrent = bencode.bdecode(bytes)
    info = torrent['info']
    #print info.keys()
    keys = ['name.utf-8','name']
    for k in keys:
        if k in info.keys():
            fileName = info[k]
            break
    print 'save ' + fileName
    fileName = os.path.join(root, fileName + '.torrent')
    f = open(fileName,'wb')
    f.write(bytes)
    f.close()
    

def printdic(d):
    for k,v in d.iteritems():
        print k
        print v
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('URL', nargs='*', help='torrent url')
    results = parser.parse_args()
    urls = results.URL
    urls.append(gclip())
    for u in urls:
        download(u)
    
if __name__ == '__main__':
    main()
    