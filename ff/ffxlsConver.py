# coding: utf-8

from xlrd import open_workbook, cellname
from xlwt import Workbook

val = []

def getVal(name):
    for a in val:
        if a[0]==name:
            return (a[1],a[2],a[3])
    return (-1,-1,None)
    
def loadOriginal(path = 'Original.xls'):
    wb = open_workbook(path)
    #print dir(wb)
    s = wb.sheet_by_index(0)
    for row in range(s.nrows):
        for col in range(s.ncols):
            v = s.cell(row,col).value
            if (v != ''):
                val.append((cellname(row,col), row, col, v))

def grc(name):# eg: B3
    i = int(name[1:]) - 1
    j = 'ABCDEFGHIJKLMN'.find(name[0])
    return (i,j)

def writeNew(path = 'simple.xls'):
    book = Workbook()
    s1 = book.add_sheet('Sheet 1')
    def write(sheet, frm, to):
        i,j,v = getVal(frm)
        i,j = grc(to)
        sheet.write(i, j, v)
    #head
    write(s1,'D1','A1')#唐山万千百货有限公司
    write(s1,'H2','A2')#门店自采验收单
    write(s1,'B3','A3')#电脑单号
    write(s1,'J3','E3')#单据编号
    write(s1,'B4','A4')#审核标志
    write(s1,'J4','E4')#到货方式
    write(s1,'B6','A5')#订单编号
    write(s1,'J6','E5')#供应商
    write(s1,'B7','A6')#经营方式
    write(s1,'J7','E6')#采购部门
    write(s1,'B8','A7')#收货门店
    write(s1,'J8','E7')#收货部门
    write(s1,'B9','A8')#制单日期
    write(s1,'J9','E8')#订货日期
    write(s1,'B10','A9')#交货日期
    write(s1,'J10','E9')#到货日期
    write(s1,'B11','A10')#发票号码
    write(s1,'J11','E10')#供应商结算依据
    write(s1,'B12','A11')#录入员
    write(s1,'J12','E11')#录入日期
    write(s1,'B13','A12')#审核员
    write(s1,'J13','E12')#审核日期
    write(s1,'B17','A13')#子库存
    write(s1,'J17','E13')#审核时间
    
    #table head
    def writeTxt(sheet,to,val):
        i,j = grc(to)
        sheet.write(i, j, val)
    writeTxt(s1,'A14',u'行号')
    writeTxt(s1,'B14',u'商品编码')
    writeTxt(s1,'C14',u'品名')
    writeTxt(s1,'E14',u'交货数量')
    writeTxt(s1,'F14',u'不含税进价')
    writeTxt(s1,'G14',u'含税进价金额')
    writeTxt(s1,'H14',u'不含税进价金额')
    writeTxt(s1,'I14',u'售价')
    writeTxt(s1,'J14',u'售价金额')
    
    #table body
    i,j,v = getVal("C20")#数据行起始
    for x in range(1000):
        if i >= 0:
            writeTxt(s1,'A' + str(15 + x), v)#行号
            
            i,j,v = getVal('F' + str(20 + x))
            writeTxt(s1,'B' + str(15 + x), v)#商品编码
            
            i,j,v = getVal('I' + str(20 + x))
            writeTxt(s1,'C' + str(15 + x), v)#品名
            
            i,j,v = getVal('R' + str(20 + x))
            writeTxt(s1,'E' + str(15 + x), v)#交货数量
            
            i,j,v = getVal('V' + str(20 + x))
            writeTxt(s1,'F' + str(15 + x), v)#不含税进价
            
            i,j,v = getVal('W' + str(20 + x))
            writeTxt(s1,'G' + str(15 + x), v)#含税进价金额
            
            i,j,v = getVal('X' + str(20 + x))
            writeTxt(s1,'H' + str(15 + x), v)#不含税进价金额
            
            i,j,v = getVal('AB' + str(20 + x))
            writeTxt(s1,'I' + str(15 + x), v)#售价
            
            i,j,v = getVal('AC' + str(20 + x))
            writeTxt(s1,'J' + str(15 + x), v)#售价金额
            
            i,j,v = getVal('C' + str(21 + x))#next
        else:
            break
    
    print getVal("C30")
    
    #table foot
    
    book.save(path)

if __name__ == '__main__':
    loadOriginal()
    writeNew()
    #print grc("C13")
