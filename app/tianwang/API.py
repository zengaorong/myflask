#coding=utf-8
import xlwt
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

conn=MySQLdb.connect(host='localhost',user='root',passwd='7monthdleo',db='leodb',charset='utf8')
cursor=conn.cursor()
count = cursor.execute('select * from Wtdel')
print 'has %s record' % count
#重置游标位置
cursor.scroll(0,mode='absolute')
#搜取所有结果
results = cursor.fetchall()

# names = cursor.execute('select * from Wtdel')
# info = cursor.fetchmany(names)
# print info

#print results
#测试代码，print results
#获取MYSQL里的数据字段
fields = cursor.description
#将字段写入到EXCEL新表的第一行
wbk = xlwt.Workbook()
sheet = wbk.add_sheet('test1',cell_overwrite_ok=True)
for ifs in range(0,len(fields)):
    sheet.write(0,ifs,fields[ifs][0])
ics=1
jcs=0
for ics in range(1,len(results)+1):
    for jcs in range(0,len(fields)):
        sheet.write(ics,jcs,results[ics-1][jcs])
    #break
wbk.save('test4.xlsx')