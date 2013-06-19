# -*- coding: utf-8 -*-
#!/usr/bin/python
import pengren

for id,name,quir in pengren.getData(270,300):
    print '%s,%s,%s' % (id,name.decode('utf-8').encode('gb2312'),quir)