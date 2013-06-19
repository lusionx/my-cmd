# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
仿 C# 的 linq
"""

class Query():
    def __init__(self,iter1):
    """an init iter"""
        self.kind = 'lst'
        self.data = list(iter1)

    def Where(self,func):
        copy = self._copy(func)
        self.data = copy
        return self

    def _copy(self,func):
        if func:
            copy = [i for i in self.data if func(i)]
            return copy
        else:
            return self.data[:]

    def Count(self,func=None):
        copy = self._copy(func)
        return len(copy)

    def Any(self,func):
        copy = self._copy(func)
        return len(copy)>0

    def ToTuple(self):
        return tuple(self.data)

    def ToList(self):
        return self.data

    def Join(self,iter2,eq_on):
"""自然连接,一般后边接 .Select(lambda (a,b) :a.name+b.name)"""
        ls=[]
        for a in self.data:
            for b in iter2:
                if eq_on(a,b):
                    ls.append((a,b))
        self.data=ls
        return self

    def LeftJoin(self,iter2,eq_on,empty=None):
"""左连接,一般后边接 .Select(lambda (a,b) :a.name+b.name)"""
        ls=[]
        for a in self.data:
            for b in iter2:
                if eq_on(a,b):
                    ls.append((a,b))
        left = [a for a,b in ls]
        for a in self.data:
            if a not in left:
                ls.append((a,empty))
        self.data=ls
        return self

    def Select(self,selector):
        self.data = map(selector,self.data)
        return self

    def __getslice__(self,i=None,j=None):
        self.data=self.data[i:j]
        return self

    def __getitem__(self,i):
        return self.data[i]

    def Sum(self,selector=None):
        copy = self._copy(selector)
        sum = 0
        for a in copy:
            sum+=a
        return sum

    def Avg(self,selector=None):
        return self.Sum(selector)/float(self.Count(selector))

    def Max(self,selector=None):
        copy = self._copy(selector)
        return max(copy)

    def Min(self,selector=None):
        copy = self._copy(selector)
        return min(copy)

    def GroupBy(self,selector):
'''分组 一般后边接 .Select(lambda a:{key:a[0],gg:a[1]}'''
        ls = []
        keys = lambda arr:[key for (key,arr2) in arr]
        group = lambda arr,k:[(key,arr) for (key,arr2) in ls if key==k ][0]
        for a in self.data:
            key = selector(a)
            if key in keys[ls]:
                group(ls,key)[1].append(a)
            else:
                ls.append((key,[a]))
        return self.data = ls

    def Distinct(self,selector):
        pass

