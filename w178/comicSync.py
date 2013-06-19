# coding:utf-8
"""
同步漫画
读取U盘上的 comicSync.log 仅同步能匹配文件夹的里的zip
"""

import os,shutil

source = u'D:\\lusionx\\Pictures\\漫画'

root = os.path.abspath(os.getcwdu())

def init():
    """初始化一份文件所有的zip包漫画路径"""
    lines = []
    for dir in os.listdir(source):
        if os.path.isdir(joinp(source,dir)):
            for zip in os.listdir(joinp(source,dir)):
                if os.path.splitext(zip)[1] == u'.zip':
                    lines.append(joinp(dir,zip).encode('utf-8'))
    lines.sort()
    f = open('comicSync.log','w')
    f.write('\n'.join(lines))
    f.close()

def joinp(a,b):
    return os.path.join(a,b)

def main():
    #u盘上的文件夹
    uDirs = [a for a in os.listdir(root) if os.path.isdir(joinp(root, a))]
    f = open('comicSync.log')
    have = [a.decode('utf-8')[:-1] for a in f.readlines()]
    f.close()
    addf = []
    for dir in uDirs:
        if os.path.isdir(joinp(source, dir)):#源上 有对应的 文件夹
            # 源文件夹 上 所有 的 zip
            szips = sorted([a for a in os.listdir(joinp(source, dir)) if os.path.splitext(a)[1] == u'.zip']) 
            for a in szips:
                f1 = os.path.join(source,dir,a)
                f2 = os.path.join(root,dir,a)
                # U日志上也没有的
                if not joinp(dir,a) in have:
                    addf.append(joinp(dir,a).encode('utf-8'))
                    print 'copy %s to %s = %s' % (f1,f2,shutil.copyfile(f1,f2))
    have = [a.encode('utf-8') for a in have]
    have.extend(addf)
    have.sort()
    f = open('comicSync.log','w')
    f.write('\n'.join(have))
    f.close()
    
if __name__ == '__main__':
    main()
    #init()