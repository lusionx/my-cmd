# coding: utf-8

import re
s = u'var g_chapter_name = "第07话";'
m = re.match(r'^var g_chapter_name = "(\S+)";$',s)
print m.group(1)