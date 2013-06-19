# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///D:\\app\\db.sqlite')

def _Session():
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    return Session()

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    app = Column(String, nullable = False)
    when = Column(DateTime, nullable = False)
    message = Column(String, nullable = False)
    
    def __init__(self, app='', msg=''):
        self.message = msg
        self.app = app
        self.when = datetime.datetime.now()

def _dbInit():
    Base.metadata.create_all(engine) 

def log(app='app', msg=''):
    ss = _Session()
    o = Log(app, msg)
    ss.add(o)
    ss.commit()


def main():
    ss = Session()
    o = Log('msg')
    ss.add(o)
    ss.commit()

if __name__ == '__main__':
    #dbInit()
    main()