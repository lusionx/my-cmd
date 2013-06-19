# -*- coding: utf-8 -*-
#!/usr/bin/python

#

import httplib2

localpath = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
sharepath = 'http://share.gs/hosts.txt'

def split(flines):
    data = []
    for line in flines:
        print line
        domain = [a for a in line.split(' ') if a != '']
        
        #data.append((domain[0],domain[1]))
    return data

def main():
    h = httplib2.Http(".cache")
    resp, content = h.request(sharepath, "GET")
    #share = split(open('.cache/share.txt'))
    #print share
    local = open(localpath).readlines()
    print local
    


if __name__ == '__main__':
    main()