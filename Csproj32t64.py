# -*- coding: utf-8 -*-
#!/usr/bin/python

PATH = u'D:/91huayi/公服'

FILES = [
        u'/BusinessLayer/BusinessLayer.csproj',
        u'/DataModule/DataModule.csproj',
        u'/HandlerLayer/HandlerLayer.csproj',
        u'/Substructure/Substructure.csproj',
        u'/Web\Web.csproj',
        u'/RemoteTraining/RemoteTraining.csproj',
        #u'/ClassWebServesTest/ClassWebServesTest.csproj'
        ]
files = [ PATH + a for a in FILES]
i=0
to = 32
for path in files:
    fr=open(path,'r')
    data=''
    for line in fr.readlines():
        if line.find('Microsoft.Practices.EnterpriseLibrary.Data.dll') > -1:
            i+=1
            if to == 64:
                data+='      <HintPath>..\\x64\Microsoft.Practices.EnterpriseLibrary.Data.dll</HintPath>\n'
            elif to == 32:
                data+='      <HintPath>..\References\Microsoft.Practices.EnterpriseLibrary.Data.dll</HintPath>\n'
        else:
            data+=line
    fr.close()
    fw=open(path,'w')
    fw.write(data)
    fw.close()
    
path = PATH + u'/DataModule/DataModule.csproj'
fr=open(path,'r')
data=''
for line in fr.readlines():
    if line.find('Oracle.DataAccess.dll') > -1:
        i+=1
        if to==64:
            data+='    <HintPath>..\\x64\Oracle.DataAccess.dll</HintPath>\n'
        elif to==32:
            data+='    <HintPath>..\References\Oracle.DataAccess.dll</HintPath>\n'
    else:
        data+=line
fr.close()
fw=open(path,'w')
fw.write(data)
fw.close()
print i
