# -*- coding: utf-8 -*-
#!/usr/bin/python
import kit
import urllib2, urllib, sys
import simplejson as json
from xml.dom.minidom import parseString
from datetime import datetime

def out(line,tup):
    try:
        print line % tup
    except UnicodeEncodeError:
        print "Sorry!can't print!UnicodeEncodeError"


def loadrss(url):
    html = urllib2.urlopen(url).read()
    dom = parseString(html)
    for item in dom.getElementsByTagName('item'):
        title = item.getElementsByTagName('title')[0].firstChild.data
        link = item.getElementsByTagName('link')[0].firstChild.data
        torrent = item.getElementsByTagName('enclosure')[0].getAttribute('url')
        pubDate = item.getElementsByTagName('pubDate')[0].firstChild.data
        pubDate = datetime.strptime(pubDate[5:-6],'%d %b %Y %H:%M:%S')
        btid = link[link.rfind('/')+1:-5]
        
        save((title,link,torrent,pubDate.strftime('%Y-%m-%d %H:%M:%S'),btid))
        out('read::%s',title)




def save(a): 
    obj = kit.exec_top_one('select * from btktpx where btid = ?',(a[-1],))
    if obj == None:
        kit.exec_non('''insert into btktpx 
            (title,link,torrent,pub_date,btid) 
            values 
            (?,?,?,?,?)''',a)
        out('----add::%s',a[0])




def get_completed(id):
    url = 'http://bt.ktxp.com/ajax.php'
    #act=torrent id=182720
    #{"leechers":"9","seeders":"4","completed":"2"}
    values = {'act':'torrent','id':id}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    try:
        obj = json.loads(response.read())
        return obj[u'completed']
    except ValueError:
        out('%s Error', (id))
        return -1

def modify_completed():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #找到 4小时 以前更新的
    sql = '''select btid from btktpx
where modify isnull or ( datetime(pub_date,'+1 months') > datetime('now','localtime')  and
datetime(modify,'+4 hours') < datetime(?))'''
    for a in kit.exec_rows(sql,(now,)):
        btid = a[0]
        cc = get_completed(btid)
        if cc == -1:
            kit.exec_non('''delete from btktpx where btid = ?''',(btid,))
            print 'id::%s delete' % btid
            continue
        kit.exec_non('''update btktpx
        set completed = ?,
            modify = ?
        where btid = ?''',(cc,now,btid))
        try:
            print 'id::%s,completed::%s' % (btid,cc)
        except Error:
            print 'no print'


def main():
    load = lambda :save(yesterday())
    #load()    
    args = []
    if len(sys.argv) > 1:
        args = sys.argv[1:]
    if 'l' in args:
        url = 'http://bt.ktxp.com/rss-sort-1.xml'
        if len(args) == 2:
            url = args[1]
        print 'load::'+url
        loadrss(url)
        a = u'读取操作完成'
        print a.encode('GBK')
    elif 'm' in args:
        modify_completed()
        a = u'更新操作完成'
        print a.encode('GBK')
    else:
        a = u'没有操作'
        print a.encode('GBK')
    print raw_input()

if __name__ == '__main__':
    main()
