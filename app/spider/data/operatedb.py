#coding=utf-8
import sys
import MySQLdb
import os
import re
import uuid
import platform
from app.leotool.readexcel import readexcel_todict

reload(sys)
sys.setdefaultencoding('utf-8')
dataname = "spider"
host='120.79.217.238'



def insert_story_todb(list):
    conn= MySQLdb.connect(
        host= '120.79.217.238',
        port = 3306,
        user='root',
        passwd='7monthdleo',
        db = dataname,
        charset='utf8'
    )
    cur = conn.cursor()
    sqli =  "insert into story(story_id,story_url,story_name,story_intro,author,story_last_chapter_url,story_last_chapter_name,story_type)value(%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(sqli,list)
    conn.commit()
    conn.close()

def insert_chapter_todb(list):
    conn= MySQLdb.connect(
        host= '120.79.217.238',
        port = 3306,
        user='root',
        passwd='7monthdleo',
        db = dataname,
        charset='utf8'
    )
    cur = conn.cursor()
    sqli =  "insert into storyChapter(chapter_id,story_id,chapter_num,chapter_name,chapter_url,chapter_text)value(%s,%s,%s,%s,%s,%s)"
    cur.execute(sqli,list)
    conn.commit()
    conn.close()

def check_chapter_todb(story_id,chapter_num):
    conn= MySQLdb.connect(
        host= '120.79.217.238',
        port = 3306,
        user='root',
        passwd='7monthdleo',
        db = dataname,
        charset='utf8'
    )
    cur = conn.cursor()
    sqli =  "select * from storyChapter where story_id=%s and chapter_num=%s"
    result = cur.execute(sqli,[story_id,chapter_num])
    conn.close()
    print type(result)
    if result==long(0):
        return False
    return True
