# -*- coding: utf-8 -*-
#!/usr/bin/python

#配合 Alx.ORM.Core 的实体生成器

from sqlalchemy import *
from sqlalchemy.orm import mapper, Session
import os
root = os.path.dirname(__file__)
constr = 'sqlite:///'+root+'/info.sqlite3'
db = create_engine(constr)
db.echo = False

class Master(object):
    pass

def tableInfo():
    infos = Table('SQLITE_MASTER', MetaData(db), autoload=True)
    tables = {}
    for a in infos.select(infos.c.name.in_(['ts_user','ct_carton'])).execute():
        print a.name
        tables[a.name] = Table(a.name, MetaData(db), autoload=True)
    return tables
    
from django.template import Template, Context
from django.conf import settings
import codecs
def main(arg):
    info = tableInfo()
    for k,v in info.items():
        #print k
        for c in v.columns:
            typemap = {
                'TEXT':'String',
                'INTEGER':'Int32'
                }
            c.systype = typemap[str(c.type)]
            s = c.type
            print str(s)
            print type(s)
            print dir(s)

    cc = {
        'namespace':'mynamespace',
        'tables':info
        }
    #return
    f = codecs.open('sqliteorm.cs','w','utf-8')
    settings.configure()
    t = Template(open('template/sqliteorm.cs').read())
    f.write(t.render(Context(cc)))
    f.close()
    
if __name__ == '__main__':
    main('')
