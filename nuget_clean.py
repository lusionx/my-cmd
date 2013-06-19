# coding: utf-8

import os
from BeautifulSoup import BeautifulStoneSoup as BS

def cleanDir(Dir):
    if not os.path.isdir(Dir):
        print Dir + ' is not a dir'
        return
    for path in os.listdir(Dir):
        filePath = os.path.join(Dir, path)
        if os.path.isfile(filePath):
            os.remove(filePath)
        elif os.path.isdir(filePath):
            cleanDir(filePath)
            os.rmdir(filePath)
        else:
            print '%s is not file ,dir ' % filePath
    #os.rmdir(Dir)

def main():
    root = os.getcwdu()
    pages = os.path.join(root, 'packages')
    f = open(os.path.join(root, 'packages', 'repositories.config'))
    xml = BS(f.read())
    f.close()
    used = []
    for res in xml.findAll('repository'):
        #print res['path']
        f = open(os.path.join(root, res['path'][3:]))
        pro = BS(f.read())
        f.close()
        for p in pro.findAll('package'):
            used.append(p['id'] + '.' + p['version'])

    #已经使用的包
    #print used

    remove = []
    for dirp in os.listdir(pages):
        path = os.path.join(pages, dirp)
        if os.path.isdir(path) and (dirp not in used):
            print 'remove: ' + dirp
            remove.append(dirp)


    for d in remove:
        path = os.path.join(pages, d)
        cleanDir(os.path.join(pages, d))
        os.rmdir(path)



if __name__ == '__main__':
    main()