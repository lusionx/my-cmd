# -*- coding: utf-8 -*-
#!/usr/bin/python

from models import *
import httplib2, os
from lxml import etree
from pyquery import PyQuery as pq

constr = 'sqlite:///'+os.path.dirname(__file__)+'/info.sqlite3'

class DB():
    def __init__(self,create=False):
        """call this before tabels models operating"""
        self.session=Context(constr).session
        
    def update(self,ch):
        sess = self.session
        ch_o = sess.query(Channel).filter(Channel.link == ch.link).first()
        i = 0
        if ch_o == None:#is a new feed
            sess.add(ch)
            i = len(ch.items)
            sess.commit()
        elif ch_o.lastBuildDate != ch.lastBuildDate:
            # add new items
            #dblinks = sess.query(Item.link).filter(Item.channel_id == ch_o.id)
            #dblinks = [a[0] for a in dblinks]
            #addlinks = [ item for item in ch.items if item.link not in dblinks]
            i=0
            #for a in addlinks:
            #    i+=1
            #    a.channel = ch_o
            #   sess.add(a)
            for a in ch.items:
                a.channel_id = ch_o.id
            sess.add_all(ch.items)
            print 'add_all'
            sess.commit()
        else:
            pass #do nothing
        return i

def loadRss(url):
    """load a rss url,return Channel instence"""
    h = httplib2.Http('.cache')
    resp, content = h.request(url, "GET")
    return content
    

def genChannel(content):
    """generate a Channel instence from content """
    channel = pq(content).children('channel')
    chl = Channel()
    chl.title = channel.children('title').html()
    chl.link = channel.children('link').html()
    chl.description = channel.children('description').html()
    chl.language = channel.children('language').html()
    chl.lastBuildDate = channel.children('lastBuildDate').html()
    chl.generator = channel.children('generator').html()
    chl.items = genItems(channel.children('item'))
    return chl

    
def genItems(itemsNode):
    """generate item list"""
    items = []
    for one in itemsNode:
        item = Item()
        one = pq(one)
        item.title = one.children('title').html()
        item.link = one.children('link').html()
        item.description = one.children('description').html()
        item.author = one.children('author').html()
        item.comments = one.children('comments').html()
        item.enclosure = one.children('enclosure').html()
        item.guid = one.children('guid').html()
        item.pubDate = one.children('pubDate').html()
        item.category = one.children('category').html()
        items.append(item)
    return items

def main(url):
    db = DB()
    c = loadRss(url)
    chl = genChannel(c)
    if chl.link:
        print 'Add %s items' % (db.update(chl),)

if __name__ == '__main__':
    url = []
    url.append('http://www.cnblogs.com/rss')
    url.append('http://bt.ktxp.com/rss-sort-1.xml')
    main(url[0])
