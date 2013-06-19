# -*- coding: utf-8 -*-
#!/usr/bin/python

"""下载nasa的每日一图"""

import httplib2
import BeautifulSoup
import datetime
import os
from models import *
constr = 'sqlite:///'+os.path.dirname(__file__)+'/info.sqlite3'

class DB():
    def __init__(self,create=False):
        """call this before tabels models operating"""
        self.session = Context(constr).session

    def info(self,url,apod=None):
        """
        url like http://apod.nasa.gov/apod/ap101227.html
        return a Apod instance
        """
        if apod is None:
            apod = Apod()
            apod.url = url
        h = httplib2.Http()
        print "load:" + url
        resp, content = h.request(url, "GET")
        soup = BeautifulSoup.BeautifulSoup(content)
        p = soup.body.center.p.nextSibling
        dir = os.path.split(url)[0] + '/'
        apod.src = dir + p.a['href']
        imgdate = p.contents[0].strip('\n ')
        apod.date = datetime.datetime.strptime(imgdate,'%Y %B %d').strftime('%Y-%m-%d')
        apod.remark = soup.body.findAll('b')[0].string.strip('\n ')
        return apod
        
        
    def download(self,imgurl):
        """from url load the img,return the bytes"""
        h = httplib2.Http()
        resp, bytes = h.request(imgurl,"GET")
        return bytes
        
        
    def updateLocal(self,limit=1):
        for apod in self.session.query(Apod)\
                        .filter(Apod.date != '').filter(Apod.local == '')\
                        .order_by(Apod.url.desc()).slice(0,limit):
            ext = os.path.splitext(apod.src)[1]
            apod.local = apod.date + '-'\
                + apod.remark.replace(' ','').replace(':','').replace('?','')\
                + ext
            if os.path.exists(root+'/nasa/'+apod.local):
                print "exists:" + apod.local
            else:
                f = open(root+'/nasa/'+apod.local, 'wb')
                print 'download:'+apod.src+'@'+apod.date
                bytes = self.download(apod.src)
                f.write(bytes)
                f.close()
            self.session.commit()
        
    def updateInfo(self,limit=10):
        """更新前几条,的基本信息,并不下载图片"""
        for a in self.session.query(Apod)\
                    .filter(Apod.date == '').filter(Apod.state == '')\
                    .order_by(Apod.url.desc()).slice(0,limit):
            try:
                self.info(a.url,a)
            except:
                a.state = 'Err'
                continue
        self.session.commit()


def loadAll():
    """以往所有图片页面索引"""
    url = 'http://apod.nasa.gov/apod/archivepix.html'
    h = httplib2.Http('.cache')
    resp, content = h.request(url, "GET")
    soup = BeautifulSoup.BeautifulSoup(content)
    dir = os.path.split(url)[0]+'/'
    urls = [dir+a['href'] for a in soup.body.b.findAll('a')]
    return urls
    

if __name__ == '__main__':
    db = DB()
    #db.updateInfo(5)
    #db.updateLocal(6)
    a = Apod()
    a.url = 'http://apod.nasa.gov/apod/ap110323.html'
    db.session.add(a)
    db.session.commit()
    #raw_input()
