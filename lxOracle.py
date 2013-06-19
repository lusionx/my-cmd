# -*- coding: utf-8 -*-
#!/usr/bin/python

"""连接oracle,并取得一些字段信息,
这里不涉及对象操作
"""

from sqlalchemy import *

def main(args):
    """oracle://user:pass@host:port/service"""
    constr = 'oracle://health_record:oracle11g@10.119.120.103:1522/oraeleven'
    db = create_engine(constr)
    db.echo = False
    metadata = MetaData(db)
    tb = Table('DIC_GENDER', metadata, autoload=True)
    for cl in tb.c:
        print cl.name
    #for rw in dic.select().limit(1).execute():
    
if __name__ == '__main__':
    main('')    


    

    
