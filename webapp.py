# -*- coding: utf-8 -*-
#!/usr/bin/python

import web, os, sys
from models import *
import json
root = os.path.dirname(__file__)
constr = 'sqlite:///'+root+'/info.sqlite3'

#这里配置的url映射是大小写敏感的 ;所以最好 类名,路径全是小写
urls = {}
urls['/favicon.ico'] ='fav'#图标
class fav:
    def GET(self):
        path = os.path.join(root,'static/favicon.ico')
        return open(path,'rb').read()

#静态文件 图片,css,js,html
#不必处理,webpy 默认映射 /static/ 路径
#但是在windows下要注意 启动程序时的路径,webpy并没有使用__file__当前路径

            
#以上是静态文件的处理,以下开始有逻辑页面
urls['/'] = 'index'#首页
class index:
    def GET(self):
        raise web.seeother('/static/v/index.html')

urls['/select/(.+)'] = 'select'#对象输出
class select:
    def GET(self,modelname):
        ss = Context(constr).session
        exec('l = ss.query('+modelname+')')
        a = dict(
                error=modelname,
                count=l.count(),
                entities = [a.tdict() for a in l],
                )
        ss.close()
        return json.dumps(a)
        
urls['/test'] = 'test'
class test:
    def POST(self):
        return 'test'+json.dumps(web.data())
    def GET(self):
        return 'test'+json.dumps(web.input())
        
dic = urls
urls = []
for k,v in dic.items():
     urls.extend([k,v])
app = web.application(urls, globals())

if __name__ == "__main__":
    #web.config.debug = False
    #print app.request('/m').data
    app.run()
