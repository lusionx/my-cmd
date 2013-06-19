# coding: utf-8

"""
将zip文件中唯一目录去掉
old.zip
    dir1
        file1
        file2
new.zip
    file1
    file2
"""

import argparse, zipfile, os

def out(ss):
    print ss

def checkZip(path):
    zf = None
    if os.path.exists(path) and os.path.isfile(path) and zipfile.is_zipfile(path) :
        zf = zipfile.ZipFile(path)
        infos = zf.infolist()
        # 1 个目录 多个文件
        if (len([a.file_size for a in infos if a.file_size == 0]) == 1 and
                len([a.file_size for a in infos if a.file_size > 0]) == len(infos) - 1):
            # 文件全在这个目录下
            ss = [a.filename.decode('gb2312') for a in infos]
            head = ss[0]
            if all([ a.find(head)==0 for a in ss[1:]]):
                return (zf,infos[1:])
    print u"文件不符合要求"
    if zf:
        zf.close()
    return (None,None)
            

def main(path):
    zf, infos = checkZip(path)
    if zf:
        path, ext = os.path.splitext(path)
        path = path+'_new'
        zf2 = zipfile.ZipFile(path+ext,'w')
        for a in infos:
            bytes = zf.read(a)
            a.filename = a.filename.split('/')[1]
            out( '%s %s' % (a.filename, a.file_size))
            zf2.writestr(a,bytes)
        zf.close()
        zf2.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('FILE', nargs=1, help='zipfile path')
    results = parser.parse_args()
    path = results.FILE[0]
    main(path)