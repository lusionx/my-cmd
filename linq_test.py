# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
测试 linq
"""
import unittest
import linq
import random

class model():
    def __init__(self,i=None):
        if i==None:
            i = random.randint(0,99)
        self.index = i
        self.name = 'nameA.'+str(i)
class model2():
    def __init__(self,i=None):
        if i==None:
            i = random.randint(0,99)
        self.index = i
        self.name = 'nameB.'+str(i)

class linqTestCase(unittest.TestCase):

    def initq(self):
        data = [i for i in xrange(10)]
        f = lambda a : a%2==0
        q = linq.Query(data[:])
        return q

    def testWhere(self):
        q = self.initq()
        f = lambda a : a%2==0
        q = q.Where(f)
        self.assertEqual(q.ToList(),[0,2,4,6,8])

    def testCount(self):
        q = self.initq()
        f = lambda a : a%2==0
        self.assertEqual(q.Count(f),5)
        self.assertEqual(q.Count(),10)

    def testAny(self):
        q = self.initq()
        f = lambda a : a%2==0
        self.assertEqual(q.Any(f),True)

    def testSelect(self):
        f = lambda a:a.name
        q=[model(),model(),model(),model(),model(),model()]
        q=linq.Query(q)
        q=q.Select(f)
        #print q.ToList()
        self.assertEqual(q.Count(),6)

    def testJoin(self):
        q=[model(1),model(2),model(4),model(6),model(8),model(9)]
        q=linq.Query(q)
        q2=[model2(1),model2(2),model2(3),model2(5),model2(7),model2(9)]
        q=q.Join(q2,lambda a,b:a.index == b.index).Select(lambda (a,b) :a.name+b.name)

        self.assertEqual(q.ToList(),['nameA.1nameB.1', 'nameA.2nameB.2', 'nameA.9nameB.9'])

    def testgetslice(self):
        q = self.initq()
        q=q[8:]
        self.assertEqual( q.ToList(),[8,9])

    def testgetitem(self):
        q = self.initq()
        self.assertEqual( q[0],0)

    def testLeftJoin(self):
        q=[model(1),model(2),model(4),model(6),model(8),model(9)]
        q=linq.Query(q)
        q2=[model2(1),model2(2),model2(3),model2(5),model2(7),model2(9)]
        q=q.LeftJoin(q2,lambda a,b:a.index == b.index,model2(0)).Select(lambda (a,b) :a.name+b.name)
        self.assertEqual(q.Count(),6)

    def testSum(self):
        q = self.initq()
        self.assertEqual(q.Sum(),45)

    def testAvg(self):
        q = self.initq()
        self.assertEqual(q.Avg(),4.5)

    def testM(self):
        q = self.initq()
        self.assertEqual(q.Max(),9)
        self.assertEqual(q.Min(),0)

if __name__ == '__main__':
    unittest.main()
