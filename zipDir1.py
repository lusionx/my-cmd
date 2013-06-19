# coding: utf-8
"""
把文件夹变成zip,且不增加路径
"""
import os
import zipfile
import argparse

def zipDir(dirpath):
    filelist = []
    fullpath = ''
    for path in os.listdir(dirpath):
        fullpath = os.path.join(dirpath, path)
        if os.path.isfile(fullpath):
            filelist.append(fullpath)
        else:
            print "except:" + fullpath
    myzip = zipfile.ZipFile(os.path.basename(dirpath) + '.zip', 'w')
    for path in filelist:
        print 'wirte %s' % path
        myzip.write(path,os.path.basename(path))
    myzip.close()

def main():#指定一个 文件夹
    parser = argparse.ArgumentParser()
    parser.add_argument('DIR', nargs=1, help='dirName')
    results = parser.parse_args()
    u = results.DIR[0]
    zipDir(u)

def mainAll():#所有文件夹
    root = os.getcwd()#os.path.dirname(__file__)
    print __file__
    fullpath = ''
    for path in os.listdir(root):
        fullpath = os.path.join(root, path)
        if os.path.isdir(fullpath) and not os.path.exists(fullpath + '.zip'):
            zipDir(fullpath)
            
if __name__ == '__main__':
    mainAll()