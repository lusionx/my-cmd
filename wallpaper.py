# -*- coding: utf-8 -*-
#!/usr/bin/python

import ctypes, os, sys, random
import Image, ImageDraw
#from lxml import etree

types = ['.jpg', '.png']
_file = os.path.split(__file__)[1]

def getWallpapers(dirpath):
    try:
        directory = os.listdir(dirpath)
    except WindowsError:
        print "Directory does not exist"
        exit(0)
    wallpapers = []
    for file in directory:
        ext = os.path.splitext(file)[1]
        if ext in types:
            wallpapers.append(os.path.join(dirpath, file))
    return wallpapers
    
def set(path):
    try:#这里可能有未知的图片格式错误,如果出错就跳过
        im = Image.open(path)
        #draw = ImageDraw.Draw(im)
        #draw.text((20,im.size[1]-20),path) 不能写中文?
        path = os.path.join(os.path.dirname(__file__), 'wallpaper.bmp')
        width, height = im.size
        if width < height:
            im = im.transpose(Image.ROTATE_90)
        im.save(path)
        #del draw
        ctypes.windll.user32.SystemParametersInfoA(20, 0, path , 0)
        return True
    except:
        return False

def main2(argv):#通过xml 获取目录
    cfg = os.path.join(os.path.dirname(__file__), 'doc/Wallpapers.xml')
    doc = etree.parse(cfg)
    pics = []
    for a in doc.getroot()[0]:
        pics.extend(getWallpapers(a.text))
    #try:
    #    i = pics.index(doc.getroot()[1].text) + 1
    #    i = i % len(pics)
    #except ValueError:
    #    i = 0
    path = random.choice(pics)
    set(path)
    print path
    #doc.getroot()[1].text = path.encode('utf-8')
    #doc.write(cfg, encoding="utf-8")

def choice(paths):
    from dblite import engine
    cnn = engine.connect()
    q = []
    sum = 0
    for row in cnn.execute("""
select message, count(*) cc from logs 
where app = ? group by message order by cc""", _file):
        q.append((row['message'],row['cc']))
        sum += row['cc']
    q = [ a[0][4:] for a in q if a[1] > sum/len(q)]
    path = random.choice(paths)
    for a in q:
        path = random.choice(paths)
        if path in q:
            continue
    return path

def main(root=u"D:/lusionx/Pictures/H和邪社"):#就用和谐社的图片
    pics = []
    for a in os.listdir(root):
        path = os.path.join(root, a)
        #print path
        if os.path.isdir(path) :
            pics.extend(getWallpapers(path))
    path = choice(pics)
    import dblite
    if set(path):
        print path.encode('gb2312')
        dblite.log(_file, u'log:' + path)
    else:
        print u'error:' + path.encode('utf-8')
        dblite.log(_file, u'error:' + path)

if __name__ == "__main__":
    #main(sys.argv)
    main()
