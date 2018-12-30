#coding=utf-8
import sys
import MySQLdb
import os
import re
import uuid
import platform

reload(sys)
sys.setdefaultencoding('utf-8')
dataname = "spider"
host='120.79.217.238'

def insert_qupu_todb(list):
    conn= MySQLdb.connect(
        host= '120.79.217.238',
        port = 3306,
        user='root',
        passwd='7monthdleo',
        db = dataname,
        charset='utf8'
    )
    cur = conn.cursor()
    sqli =  "insert into scores(id,created_time,name,old_url,provider,provider_url,anime,score_text,opreat_type)value(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    print sqli
    cur.execute(sqli,list)
    conn.commit()
    conn.close()

def check_qupu_todb(id):
    conn= MySQLdb.connect(
            host= '120.79.217.238',
            port = 3306,
            user='root',
            passwd='7monthdleo',
            db = dataname,
            charset='utf8'
        )
    cur = conn.cursor()
    sqli =  "SELECT * from scores WHERE id =%s"
    result = cur.execute(sqli,[id])
    if result:
        return True
    else:
        return False