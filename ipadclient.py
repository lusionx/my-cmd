# -*- coding: utf-8 -*-
#!/usr/bin/python

import BeautifulSoup, httplib2, urllib

service = 'http://118.26.192.93:8080/ServiceTest.asmx/'


def DoFunction(limitsCode, requestCode, jsonPama):
    url = service+'DoFunction'
    body = dict( limitsCode=limitsCode,requestCode=requestCode,jsonPama=jsonPama )
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    http = httplib2.Http()
    response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
    return BeautifulSoup.BeautifulSoup(content)

def GetFunctionParam(requestCode):
    url = service+'GetFunctionParam'
    body = dict( requestCode=requestCode )
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    http = httplib2.Http()
    response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
    return BeautifulSoup.BeautifulSoup(content)

def LoginOut(limitsCode):
    url = service+'LoginOut'
    body = dict( limitsCode=limitsCode )
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    http = httplib2.Http()
    response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
    return BeautifulSoup.BeautifulSoup(content)

import json

def getVal(s):
    a = s.find('string').string
    return a

def pp(d):
    for k,v in d.items():
        print k + ':' + v

if __name__ == '__main__':
    a = GetFunctionParam('Sub041')
    #a = DoFunction('','F0001','{"MachineCode":"e26e42f8238b7a3bf09722fa50f8b5c192dde47e","LogingId":"yfwsy","Pwd":"123456"}')
    #a = DoFunction('xx-89f21fdc-7621-4baf-a531-0fce9a2d8a98-79406','Sub040','e834165f-c4e4-4cfa-9122-dc51e2627102')
    a = DoFunction('xx-89f21fdc-7621-4baf-a531-0fce9a2d8a98-79406','Sub041','["e834165f-c4e4-4cfa-9122-dc51e2627102","510682109"]')
    print getVal(a)
