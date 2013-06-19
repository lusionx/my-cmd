# -*- coding: utf-8 -*-
#!/usr/bin/python

"""生成 web服务访问代理
"""
import BeautifulSoup as bsp
import httplib2
import os

#endwith .asxm
service = 'http://124.205.94.73:8001/ServiceTest.asmx'

def methods():
    h = httplib2.Http('.cache')
    resp, content = h.request(service, "GET")
    soup = bsp.BeautifulSoup(content)
    lis = soup.findAll('li')
    #print soup.findAll('li')
    dir = os.path.split(service)[0]+'/'
    hrefs = map(lambda li:dir + li.a['href'],lis)
    return hrefs

def methodInfo(url):
    h = httplib2.Http('.cache')
    resp, content = h.request(url, "GET")
    soup = bsp.BeautifulSoup(content)
    form = soup.form
    action = form['action']
    name = os.path.split(action)[1]
    pars = [a['name'] for a in form.findAll('input',type='text')]
    return name, action, pars


from django.template import Template, Context
from django.conf import settings
import codecs

def main():
    f = codecs.open('client.py','w','utf-8')
    settings.configure()
    cc = dict(service=service,methods=[])
    mds = cc['methods']
    for a in methods():
        name, action, pars = methodInfo(a)
        mds.append(dict(name=name, action=action,
            pars=', '.join(pars),
            body=','.join([ a+'='+a for a in pars])))
    t = Template(open('template/WebClient.txt').read())
    f.write(t.render(Context(cc)))
    f.close()

if __name__ == '__main__':
    main()
