# -*- coding: utf-8 -*-
#!/usr/bin/python

"""sqlalchemy 使用示例代码
"""
from sqlalchemy import *

db = create_engine('sqlite:///info.sqlite3')
db.echo = True
metadata = MetaData(db)

def run(stmt):
    rs = stmt.execute()
    for row in rs:
        print row

def createTable():
    users = Table('users', metadata,
        Column('user_id', Integer, primary_key=True),
        Column('name', String(40)),
        Column('age', Integer),
        Column('password', String),
    )
    #users.create()
    i = users.insert()
    i.execute(name='Mary', age=30, password='secret')
    i.execute({'name': 'John', 'age': 42},
              {'name': 'Susan', 'age': 57},
              {'name': 'Carl', 'age': 33})

    s = users.select()
    rs = s.execute()

    row = rs.fetchone()
    print 'Id:', row[0]
    print 'Name:', row['name']
    print 'Age:', row.age
    print 'Password:', row[users.c.password]
    for row in rs:
        print row.name, 'is', row.age, 'years old'
        
    emails = Table('emails', metadata,
    Column('email_id', Integer, primary_key=True),
    Column('address', String),
    Column('user_id', Integer, ForeignKey('users.user_id')),
    )
    #emails.create()
    i = users.insert()
    i.execute(
        {'name': 'Mary', 'age': 30},
        {'name': 'John', 'age': 42},
        {'name': 'Susan', 'age': 57},
        {'name': 'Carl', 'age': 33}
    )
    i = emails.insert()
    i.execute(
        # There's a better way to do this, but we haven't gotten there yet
        {'address': 'mary@example.com', 'user_id': 1},
        {'address': 'john@nowhere.net', 'user_id': 2},
        {'address': 'john@example.org', 'user_id': 2},
        {'address': 'carl@nospam.net', 'user_id': 4},
    )

def selectStatements():

    # The users table already exists, so no need to redefine it. Just
    # load it from the database using the "autoload" feature.
    users = Table('users', metadata, autoload=True)

    # Most WHERE clauses can be constructed via normal comparisons
    s = users.select(users.c.name == 'John')
    run(s)
    s = users.select(users.c.age < 40)
    run(s)

    # Python keywords like "and", "or", and "not" can't be overloaded, so
    # SQLAlchemy uses functions instead
    s = users.select(and_(users.c.age < 40, users.c.name != 'Mary'))
    run(s)
    s = users.select(or_(users.c.age < 40, users.c.name != 'Mary'))
    run(s)
    s = users.select(not_(users.c.name == 'Susan'))
    run(s)

    # Or you could use &, | and ~ -- but watch out for priority!
    s = users.select((users.c.age < 40) & (users.c.name != 'Mary'))
    run(s)
    s = users.select((users.c.age < 40) | (users.c.name != 'Mary'))
    run(s)
    s = users.select(~(users.c.name == 'Susan'))
    run(s)

    # There's other functions too, such as "like", "startswith", "endswith"
    s = users.select(users.c.name.startswith('M'))
    run(s)
    s = users.select(users.c.name.like('%a%'))
    run(s)
    s = users.select(users.c.name.endswith('n'))
    run(s)

    # The "in" and "between" operations are also available
    s = users.select(users.c.age.between(30,39))
    run(s)
    # Extra underscore after "in" to avoid conflict with Python keyword
    s = users.select(users.c.name.in_(['Mary', 'Susan']))
    run(s)

    # If you want to call an SQL function, use "func"
    s = users.select(func.substr(users.c.name, 2, 1) == 'a')
    run(s)

    # You don't have to call select() on a table; it's got a bare form
    s = select([users], users.c.name != 'Carl')
    run(s)
    s = select([users.c.name, users.c.age], users.c.name != 'Carl')
    run(s)

    # This can be handy for things like count()
    s = select([func.count(users.c.user_id)])
    run(s)
    # Here's how to do count(*)
    s = select([func.count("*")], from_obj=[users])
    run(s)
    
def joins():

    users = Table('users', metadata, autoload=True)

    emails = Table('emails', metadata, autoload=True)

    # This will return more results than you are probably expecting.
    s = select([users, emails])
    run(s)

    # The reason is because you specified no WHERE clause, so a full join was
    # performed, which returns every possible combination of records from
    # tables A and B. With an appropriate WHERE clause, you'll get the
    # restricted record set you really wanted.
    s = select([users, emails], emails.c.user_id == users.c.user_id)
    run(s)

    # If you're interested in only a few columns, then specify them explicitly
    s = select([users.c.name, emails.c.address],
               emails.c.user_id == users.c.user_id)
    run(s)

    # There are also "smart" join objects that can figure out the correct join
    # conditions based on the tables' foreign keys
    s = join(users, emails).select()
    run(s)

    # If you want all the users, whether or not they have an email address,
    # then you want an "outer" join.
    s = outerjoin(users, emails).select()
    run(s)

    # Order of outer joins is important! Default is a "left outer join", which
    # means "all records from the left-hand table, plus their corresponding
    # values from the right-hand table, if any". Notice how this time, Susan's
    # name will *not* appear in the results.
    s = outerjoin(emails, users).select()
    run(s)

def mysqldb():
    db = create_engine('mysql://root:444444@127.0.0.1:3306/alx',encoding='utf8')
    db.echo = False
    proxy = Table('proxy', MetaData(db), autoload=True)
    s = proxy.select()
    run(s)

from sqlalchemy.orm import *
def mapping():

    users = Table('users', metadata, autoload=True)
    emails = Table('emails', metadata, autoload=True)

    # These are the empty classes that will become our data classes
    class User(object):
        pass
    class Email(object):
        pass

    usermapper = mapper(User, users)
    emailmapper = mapper(Email, emails)

    session = Session()

    mary = session.query(User).filter(User.name=='Mary').first()
    mary.age += 1

    session.flush()

    fred = User()
    fred.name = 'Fred'
    fred.age = 37

    print "About to flush() without a save()..."
    session.commit()  # Will *not* save Fred's data yet

    session.add(fred)
    print "Just called save(). Now flush() will actually do something."
    session.commit()  # Now Fred's data will be saved

    session.delete(fred)
    session.commit()

def main():
    mapping()

if __name__ == '__main__':
    main()

