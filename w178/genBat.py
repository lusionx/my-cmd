# coding: utf-8

import argparse, json, os

def main():
    dir = os.path.dirname(__file__)
    if dir == '':
        dir = os.getcwd()
    for name in os.listdir(dir):
        fpath = os.path.join(dir,name)
        #print os.path.splitext(name)[1]
        if os.path.isfile(fpath) and os.path.splitext(name)[1] == '.py':
            f = open(os.path.join(dir,os.path.splitext(name)[0])+'.bat','w')
            f.write('python ')
            f.write(fpath)
            f.write(' %1 %2 %3 %4 %5')
            f.close()
if __name__ == '__main__':
    #print os.getcwd()
    #print __file__
    main()