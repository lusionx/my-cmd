# -*- coding: utf-8 -*-
#!/usr/bin/python

'''合并几个css文件,为一个文件'''
import kit
import re
source =[u'D:\91huayi\健康档案\RemoteTraining\css\common.css'
        ]

target = u'c:\merge.css'

text = ''

for a in source:
    f = open(a)
    text+=kit.trim(f.read())
    f.close()

text = text.replace('\n','')
text = text.replace('\t','')

has = True
while has:
    if text.find('  ') > -1:
        text = text.replace('  ',' ')
    else:
        has = False
        
text = text.replace('}','}\n')

p = re.compile( '/\*.*\*/')
text = p.sub('',text)
print text
f = open(target,'w')
f.write(text)
f.close()
