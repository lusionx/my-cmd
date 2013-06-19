# -*- coding: utf-8 -*-
#!/usr/bin/python

'''
将此文件放在某处执行,将生成所在文件夹下所有文件的列表,
默认排除隐藏文件
'''

import os

filelist=[]

def sanc_dir(dirpath, dirname):
    isdir = dirname in ('.svn','obj','HTML_Test','test')
    return not isdir
    
def include_file(dirpath, filename):
    f,ext=os.path.splitext(filename)
    return ext == '.aspx'


def scan(dirpath):
    for path in os.listdir(dirpath):
        fullpath = os.path.join(dirpath, path)
        if os.path.isdir(fullpath) and sanc_dir(dirpath, path):
            scan(fullpath)
        elif os.path.isfile(fullpath) and include_file(dirpath, path):
            filelist.append(fullpath)
        else:
            pass


def main():
    dir =u'D:\91huayi\健康档案\Web'
    scan(dir)
    for path in map(lambda a:a[len(dir):],filelist):
        print '~'+path

if __name__ == '__main__':
    main()
