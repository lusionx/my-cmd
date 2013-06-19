#coding: utf-8

"""
使用python 下载 npmjs.org的模块
"""

import httplib2, json, os, tarfile, sys, os

cfg = {}
cfg['target'] = os.environ['NODE_PATH']
cfg['download'] = os.path.abspath(os.path.join(cfg['target'], '..\\', 'tmp'))
cfg['childPkg'] = []

def cleanDir(Dir):
    if not os.path.isdir(Dir):
        print 'is not a dir'
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

def cmpVersion(v1, v2):
    """
    比较 *(0.0.1), none(0.0.0), latest(9.9.9), x.x.x 作为版本号时的大小 as cmp
    """
    def fix(v):
        sp = '~>='
        for s in sp:
            v = v.replace(s,'')
        v = v.replace('x','0')
        if v == '*':
            return [0,0,1]
        if v == 'none':
            return [0,0,0]
        if v == 'latest':
            return [9,9,9]
        v = [int(a) for a in v.split('.')]
        for i in xrange(len(v), 3):
            v.append(0)
        return v
    v1 = fix(v1)
    v2 = fix(v2)
    for i in xrange(0,3):
        if v1[i] == v2[i]:
            continue
        else:
            return cmp(v1[i], v2[i])
    return 0


def install(nname, ver='latest'):
    url = 'http://registry.npmjs.org/' + nname

    #分析json 得到最新版的地址,版本号
    print 'Get package info from %s' % url
    h = httplib2.Http()
    resp, content = h.request(url, "GET")
    info = json.loads(content)

    #可能有找不到的情况
    if info.has_key('error'):
        print "Can't find %s" % nname
        return

    if ver =='latest':
        ver = info['dist-tags']['latest']

    if not info['versions'].has_key(ver):
        print "Can't find %s version %s" % (nname, ver)
        return

    print 'Get verson %s' % ver

    lastverson = info['versions'][ver]
    url = lastverson['dist']['tarball']

    #处理依赖 队列
    if lastverson.has_key('dependencies'):
        analysisDependencies(lastverson['dependencies'])

    downLoad(url, nname, ver)
    print 'install ' + nname + ' v' + ver + ' finished!'

def downLoad(url, nname, ver):
    #下载 tgz文件
    print 'Download from %s' % url
    h = httplib2.Http()
    filename = os.path.basename(url)
    if not os.path.isfile(filename):
        resp, content = h.request(url,'GET')
        f = open(os.path.join(cfg['download'], filename),'wb')
        f.write(content)
        f.close()

    #先删除目标目录
    if os.path.isdir(os.path.join(cfg['target'], nname)):
        cleanDir(os.path.join(cfg['target'], nname))
        os.rmdir(os.path.join(cfg['target'], nname))

    #解压 tgz文件
    print 'Extracting'
    tar = tarfile.open(os.path.join(cfg['download'], filename))
    for mem in tar.getmembers():
        if not mem.isfile():
            continue
        name = mem.name
        ff = tar.extractfile(mem)
        tf = os.path.join(cfg['target'], nname, name[8:])
        if not os.path.isdir(os.path.dirname(tf)):
            os.makedirs(os.path.dirname(tf))
        tf = open(os.path.join(cfg['target'], nname, name[8:]), 'wb')
        tf.write(ff.read())
        ff.close()
        tf.close()
    tar.close()


def analysisDependencies(dpd):
    for k,v in dpd.items():
        localv = 'none'
        path = os.path.join(cfg['target'], k, 'package.json')
        if os.path.isfile(path):
            f = open(path)
            localv = json.loads(f.read())['version']
            f.close()
        print '    require %s %s : local %s ' % (k, v, localv)

        try:
            need = cmpVersion(v, localv)
        except Exception, e:
            need = 1
            msg = 'cmp error: %s - %s' % (v, localv)
            print msg
            open('npm_cmpV_error.txt', 'w').write(msg)
        if need == 1:
            print '        %s append' % k
            cfg['childPkg'].append(k)


def remove(nname):
    dirpath = os.path.join(cfg['target'], nname)
    if os.path.isdir(dirpath):
        cleanDir(dirpath)
        os.rmdir(dirpath)
        print 'Remove %s from lib(%s)' % (nname, cfg['target'])
        return True
    else:
        print "Can't find %s from lib(%s)" % (nname, cfg['target'])
        return False

def localPkgInf(nname):
    path = os.path.join(cfg['target'], nname, 'package.json')
    if os.path.isfile(path):
        f = open(path)
        info = json.loads(f.read())
        f.close()
        if not info.has_key('description'):
            info['description'] = 'None'
        if not info.has_key('dependencies'):
            info['dependencies'] = {}
        return info

def show(name):
    def lblank(i):
        bk=''
        for e in range(i):
            bk += '    '
        return bk

    def showone(nname,deep = 0):
        info = localPkgInf(nname)
        if info is None:
            print 'Cant find ' + nname
            return
        keys = ['name','version','description']
        for k in keys:
            print lblank(deep),
            print '%s : %s' % (k, info[k])
        print lblank(deep),
        print 'dependencies:'
        for k,v in info['dependencies'].items():
            if localPkgInf(k):
                print lblank(deep + 1),
                print '%s : %s (%s)' % (k, v, localPkgInf(k)['version'])
                showone(k, deep + 2)
            else:
                print lblank(deep + 2),
                print '%s : %s (%s)' % (k, v, 'None')
        print ''
    if name == 'all':
        i = 0
        for path in os.listdir(cfg['target']):
            if os.path.isdir(os.path.join(cfg['target'],path)) and path[0] != '.':
                showone(path)
                i+=1
        print 'There are %d packages.' % i
    else:
        showone(name)


import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', action="store_true", help='remove pkg')
    group.add_argument('-i', action="store_true", help='install pkg')
    group.add_argument('-s', action="store_true", help='show pkg')
    parser.add_argument('PKG', nargs=1, help='pkg name')
    parser.add_argument('-v', default='latest', metavar='x.x.x', help = 'version for install')
    results = parser.parse_args()
    if results.r:
        remove(results.PKG[0])
    if results.i:
        install(results.PKG[0], results.v)
        while len(cfg['childPkg']) > 0:
            a = cfg['childPkg'][0]
            del cfg['childPkg'][0]
            install(a)
    if results.s:
        show(results.PKG[0])

