# -*- coding: utf-8 -*-
#!/usr/bin/python

"""连接oracle,并取得一些字段信息,
这里不涉及对象操作
"""

from sqlalchemy import *

class DB:
    def __init__(self):
        constr = 'mysql://root:444444@127.0.0.1:3306/test'
        db = create_engine(constr)
        db.echo = False
        self.meta = MetaData(db)
        table = {}
        table['user'] = Table('user', self.meta,
            Column('id', String(36), primary_key=True),
            Column('name', String(128), nullable=False, default=''),
            Column('email', String(128), nullable=False, default=''),
            Column('age', Integer, nullable=False, default=0),
            Column('password', String(128), nullable=False, default=''),
        )
        self.table = table
        
    def create(self):
        for k,t in self.table.items():
            t.create()


def main(args):
    db = DB()
    db.create()

if __name__ == '__main__':
    main('')
