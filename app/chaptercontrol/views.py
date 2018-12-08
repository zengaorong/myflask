#coding=utf-8

from flask import render_template, redirect, request, url_for, flash,jsonify,send_from_directory,\
    current_app
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import chaptercontrol
from ..models import Manhua,Chapter
from sqlalchemy import and_
from datetime import  datetime
import uuid
from .. import db
import sys
import urllib
import os
import time
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from app import models
import shutil
import platform


reload(sys)
sys.setdefaultencoding('utf-8')



# 后台展示漫画的列表 这里的列表构建需要再研究下
@chaptercontrol.route('/chapterlist', methods=['GET', 'POST'])
def chapterlist():
    page = request.args.get('page', 1, type=int)
    mhid = request.args.get('mhid', "", type=str)
    # 使用and__测试联合查询  mhid
    pagination = Chapter.query.filter_by(mhname_id=mhid).order_by(Chapter.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items



    listsize = pagination.total
    return render_template('chaptercontrol/chapterlist.html',posts=posts,pagination=pagination,listsize=listsize,mhid=mhid)




# ajax 获取图片列表
@chaptercontrol.route('/getpicslist', methods=['GET', 'POST'])
def getpicslist():
    chapterid = request.args.get('chapterid', '', type=str)
    page = request.args.get('page', '', type=int)
    pagesize = current_app.config['FLASKY_POSTS_PER_PAGE']
    totalnum = 0

    if(chapterid!=""):
        chapter = Chapter.query.filter_by(id=chapterid).first()
        picslist = chapter.data.split('\n')
        totalnum = len(picslist) - 1
        if(totalnum/pagesize>=(page+1)):
            showlist = picslist[page*pagesize:(page+1)*pagesize]
        else:
            showlist = picslist[-(totalnum%pagesize+1):-1]
    return jsonify(picslist=showlist,pagesize=pagesize,totalnum=totalnum)


# 删除漫画图片
@chaptercontrol.route('/deletepics', methods=['POST'])
def deletepics():
    id = request.form.get('id', "", type=str)
    chapter = Chapter.query.filter_by(id = id).first()
    chapter.data = ""
    db.session.add(chapter)
    db.session.commit()
    return jsonify("ok","123")


# 添加漫画章节
@chaptercontrol.route('/chapterfrom', methods=['GET', 'POST'])
def chapterfrom():
    id = request.args.get('id', "", type=str)
    mhname_id = request.args.get('mhname_id', "", type=str)
    picsname = None
    has_data = False
    if(id!=""):
        #chapter = Chapter.query.filter_by(id=id)

        chapter_latest = db.session.query(Chapter.id,Chapter.mhname_id,Manhua.mhname,Chapter.chapter_nums,Chapter.data,Chapter.chapter_name).outerjoin(Manhua,Manhua.id == Chapter.mhname_id ).filter(Chapter.id == id).first()

        if(chapter_latest.data!=""):
            has_data = True

        return render_template('chaptercontrol/chapterfrom.html',chapter=chapter_latest,has_data=has_data)
    else:
        # 获取漫画类
        manhua = Manhua.query.filter_by(id=mhname_id).first()
        # chapter_latest = Chapter.query.order_by(Chapter.chapter_nums.asc()).filter_by(mhname_id=mhname_id).first()
        # if(chapter_latest!=None):
        #     print chapter_latest.chapter_nums

        chapter = Chapter(id=None,mhname_id=mhname_id,chapter_nums=0,chapter_name="",)

        # 这里使用不到联合查询 只需要带些信息过去
        # chapter = Chapter(id=None,mhname_id=mhname_id,chapter_nums="",chapter_name="")
        # chapter_union = db.session.query(Chapter.id,Chapter.mhname_id,Manhua.mhname,Chapter.chapter_nums).outerjoin(Manhua,Manhua.id == Chapter.mhname_id ).filter(Manhua.id==mhname_id)
        #
        # # chapter_union = Chapter.query.outerjoin(Manhua)
        # print chapter_union
        # for key in chapter_union:
        #     print key
        return render_template('chaptercontrol/chapterfrom.html',chapter=chapter,manhua=manhua)


# 添加漫画章节
@chaptercontrol.route('/chapterpicfrom', methods=['GET', 'POST'])
def chapterpicfrom():
    id = request.args.get('id', "", type=str)
    mhname_id = request.args.get('mhid', "", type=str)
    picsname = None
    has_data = False
    if(id!=""):
        chapter_latest = db.session.query(Chapter.id,Chapter.mhname_id,Manhua.mhname,Chapter.chapter_nums,Chapter.data,Chapter.chapter_name).outerjoin(Manhua,Manhua.id == Chapter.mhname_id ).filter(Chapter.id == id ).first()

        if(chapter_latest.data!="" and chapter_latest.data!=None):
            has_data = True

        return render_template('chaptercontrol/chapterpicfrom.html',chapter=chapter_latest,has_data=has_data)



@chaptercontrol.route('/save', methods=['POST'])
def save():
    mhname = request.form.get('mhname', "", type=str)
    mhid = request.form.get('mhid', "", type=str)
    chapterid = request.form.get('id', "", type=str)
    mhurl = request.form.get('mhurl', "", type=str)
    chapternum = request.form.get('chapternum', 0, type=int)
    chaptername = request.form.get('chaptername', "", type=str)
    base64data = request.form.get('base64data', "", type=str)
    if(chapterid!="" and chapterid!='None'):
        chapter = Chapter.query.filter_by(id=chapterid).first()
        dt = datetime.now()
        chapter.updata_time = dt.strftime( '%Y-%m-%d %H:%M:%S' )
        chapter.chapter_name = chaptername
        chapter.chapter_nums = chapternum
    else:
        dt = datetime.now()
        time = dt.strftime( '%Y-%m-%d %H:%M:%S' )
        chapterid = uuid.uuid1()
        chapter = Chapter(id=chapterid,mhname_id=mhid,chapter_nums=chapternum,chapter_name=chaptername,creat_time=time,updata_time=time,)

    db.session.add(chapter)
    db.session.commit()
    #return redirect(url_for('mhcontrol.manhualist'))

    manhua = Manhua.query.filter_by(id=mhid).first()

    return redirect(url_for('chaptercontrol.chapterlist') + '?mhid=' + mhid )




@chaptercontrol.route('/chapterdelete', methods=['get'])
def chapterdelete():
    id = request.args.get('id', "", type=str)
    mhid = request.args.get('mhid', "", type=str)

    chapter_latest = db.session.query(Chapter.id,Chapter.mhname_id,Manhua.mhname,Chapter.chapter_nums,Chapter.data,Chapter.chapter_name).outerjoin(Manhua,Manhua.id == Chapter.mhname_id ).filter(Chapter.id == id ).first()

    if(chapter_latest.data == None):
        chapter = Chapter.query.filter_by(id=id).first()
        db.session.delete(chapter)
        db.session.commit()
        return redirect(url_for('chaptercontrol.chapterlist') + '?mhid=' + mhid)
    pic_list = chapter_latest.data.split('\n')
    chaptername = chapter_latest.chapter_name
    mhname = chapter_latest.mhname


    cwd = os.getcwd()
    dir = '/app/static/pics/'
    test_str = (cwd + '/app/static/pics/' + mhname + '/' + chaptername)

    if(platform.system()=='Windows'):
        test_str = test_str.replace("\\",'/')

    if(os.path.exists(test_str)):
        shutil.rmtree(test_str)
        chapter = Chapter.query.filter_by(id=id).first()
        db.session.delete(chapter)
        db.session.commit()


    return redirect(url_for('chaptercontrol.chapterlist') + '?mhid=' + mhid)


# upload
@chaptercontrol.route('/upload', methods=['get'])
def upload():
    # mhname = request.form.get('mhname', "", type=str)
    # id = request.form.get('mhid', "", type=str)
    # mhurl = request.form.get('mhurl', "", type=str)
    # base64data = request.form.get('base64data', "", type=str)
    # 图片名称 章节id
    id = request.args.get('chapterid', "", type=str)
    mhurl = request.args.get('pic_url', "", type=str)

    chapter = Chapter.query.filter_by(id=id).first()

    manhua = Manhua.query.filter_by(id = chapter.mhname_id).first()
    # picslist = chapter.data.split('\n')
    #
    # class Address:
    #     def __init__(self, home, office):
    #         self.home = home
    #         self.office = office
    # # def __repr__(self):
    # #     return repr((self.name, self.grade, self.age))
    #
    # class Customer:
    #     def __init__(self, name, grade, age, home, office):
    #         self.name = name
    #         self.grade = grade
    #         self.age = age
    #         self.address = Address(home, office)
    #     # def __repr__(self):
    #     #     return repr((self.name, self.grade, self.age, self.address.home, self.address.office))
    #
    # customers = [
    #     Customer('john', 'A', 15, '111', 'aaa'),
    #     Customer('jane', 'B', 12, '222', 'bbb'),
    #     Customer('dave', 'B', 10, '333', 'ccc'),
    # ]
    #
    #
    #
    # print (mhurl in picslist)
    # print type(chapter)
    # print jsonify(picslist)
    # print json.dumps(customers,default=lambda obj: obj.__dict__,sort_keys=True)
    # print isinstance(chapter,Chapter)
    dicts = json.dumps(chapter,cls=AlchemyJsonEncoder)
    # print dicts
    # print type(dicts)
    # print json.dumps(dicts)

    map_data = {"id":id,"mhurl":mhurl,"upfileurl":"/api/uploadtempImage","fileurl":"upload/temp","chaptername":chapter.chapter_name,"manhuaname":manhua.mhname}

    # print json.dumps(map_data)

    return render_template('chaptercontrol/upload.html',chapter=json.dumps(map_data))


def mymovefile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print "%s not exist!"%(srcfile)
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        print "move %s -> %s"%( srcfile,dstfile)


@chaptercontrol.route('/addpic',methods=['post'])
def addpic():
    id = request.form.get('id','',str)
    mhurl = request.form.get('mhurl','',str)
    upfileurl = request.form.get('upfileurl','',str)
    fileurl = request.form.get('fileurl','',str)
    responsurl = request.form.get('responsurl','',str)

    chaptername = request.form.get('chaptername','',str)
    manhuaname = request.form.get('manhuaname','',str)

    # 先判读是否是该漫画的url
    chapter = Chapter.query.filter_by(id = id).first()
    pic_list = chapter.data.split('\n')

    position = pic_list.index(mhurl) if mhurl in pic_list else None
    if(position!=None):
        pic_list.insert(position,responsurl)


        cwd = os.getcwd()
        dir = '/app/static/pics/'
        #test_str = "家庭教师/2 死气弹无法使用/2 死气弹无法使用15.jpg"
        test_str = responsurl


        srcfile=(cwd + '/app/static/upload/temp/' + test_str.decode('utf-8'))
        dstfile=(cwd + '/app/static/pics/' + test_str.decode('utf-8'))
        test_str_unicode_check = (cwd + '/app/static/upload/temp/' + test_str.decode('utf-8'))
        # print repr(test_str_unicode_check)
        print os.path.isfile(srcfile.replace('xa0'," "))
        print os.path.isfile((cwd + '/app/static/upload/temp/' + "家庭教师/2 死气弹无法使用/2 死气弹无法使用15.jpg".decode('utf-8')))
        print repr(srcfile.replace(u'\xa0', u' ',-1))
        print repr((cwd + '/app/static/upload/temp/' + "家庭教师/2 死气弹无法使用/2 死气弹无法使用15.jpg".decode('utf-8')))

        test_check = srcfile.replace(u'\xa0', u' ',-1)
        test_check = test_check.replace(u' ', u'\xa0',1)
        #test_check = srcfile.replace(u' ', u'\xa0',1)
        print repr(test_check)

        mymovefile(test_check,dstfile)

        pic_url_removed = ""
        # 用于判断循环最后一位 去除'\n'
        temp_num = 1
        for key in pic_list:
            if(len(pic_list)==temp_num):
                pic_url_removed = pic_url_removed + key
            else:
                pic_url_removed = pic_url_removed + key + '\n'

            temp_num = temp_num + 1
        chapter.data = pic_url_removed
        db.session.add(chapter)
        db.session.commit()



    return jsonify('ok','123')



class AlchemyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # 判断是否是Query
        record = {}
        if isinstance(obj.__class__, DeclarativeMeta):
            # 定义一个字典数组
            fields = []
            # 定义一个字典对象

            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    record[field] = data
                except TypeError:
                    record[field] = None
            # a json-encodable dict
            return record

        return None




# 对图片文件的移动 添加 删除逻辑操作  接收漫画的id和章节的id
@chaptercontrol.route('/operate',methods=['post'])
def operate():
    operate_type = request.form.get('operatetype','',str)
    chapter_id = request.form.get('chapterid','',str)
    manhua_id = request.form.get('manhuaid','',str)
    pic_url = request.form.get('pic_url','',str)
    page = request.form.get('page','',int)

    chapter = Chapter.query.filter_by(id=chapter_id).first()
    picslist = chapter.data.split('\n')

    # for key in picslist:
    #     print key


    # type = 1 上移 type = 2 下移 type = 3 删除 type = 4 插入

    cwd = os.getcwd()
    dir = '/app/static/pics/'
    test_str = pic_url
    position = picslist.index(pic_url) if pic_url in picslist else None
    if(operate_type=="1"):
        if(len(picslist)>=2 and position!=0):
            picslist[position],picslist[position-1] = picslist[position-1],picslist[position]
            pic_url_moved_up = ""
            temp_num = 1
            for key in picslist:
                if(len(picslist)==temp_num):
                    pic_url_moved_up = pic_url_moved_up + key
                else:
                    pic_url_moved_up = pic_url_moved_up + key + '\n'

                temp_num = temp_num + 1
            chapter.data = pic_url_moved_up

            db.session.add(chapter)
            db.session.commit()

    if(operate_type=="2"):
        if(len(picslist)>=2 and position!=len(picslist)-1):
            picslist[position],picslist[position+1] = picslist[position+1],picslist[position]
            pic_url_moved_up = ""
            temp_num = 1
            for key in picslist:
                if(len(picslist)==temp_num):
                    pic_url_moved_up = pic_url_moved_up + key
                else:
                    pic_url_moved_up = pic_url_moved_up + key + '\n'

                temp_num = temp_num + 1
            chapter.data = pic_url_moved_up

            db.session.add(chapter)
            db.session.commit()






    if(operate_type=="3"):
        test_str_unicode_check = (cwd + '/app/static/pics/' + test_str.decode('utf-8'))
        print repr(test_str_unicode_check)
        print os.path.isfile(test_str_unicode_check)

        test_check = test_str_unicode_check.replace(u'\xa0', u' ',-1)
        test_check = test_check.replace(u' ', u'\xa0',1)
        print os.path.isfile(test_check)

        if( os.path.isfile(test_str_unicode_check) == os.path.isfile(test_check) == False ):
            return jsonify("error",'123')
        if(test_str in picslist):
            picslist.remove(test_str)
            pic_url_removed = ""
            # 用于判断循环最后一位 去除'\n'
            temp_num = 1
            for key in picslist:
                if(len(picslist)==temp_num):
                    pic_url_removed = pic_url_removed + key
                else:
                    pic_url_removed = pic_url_removed + key + '\n'

                temp_num = temp_num + 1
            chapter.data = pic_url_removed

            if( os.path.isfile(test_str_unicode_check)):
                os.remove(test_str_unicode_check)
            else:
                os.remove(test_check)
            db.session.add(chapter)
            db.session.commit()



    pagesize = current_app.config['FLASKY_POSTS_PER_PAGE']

    if(chapter!=""):
        picslist = chapter.data.split('\n')
        totalnum = len(picslist) - 1
        print type(totalnum/pagesize)
        print type(page)

        if(totalnum/pagesize>=(page+1)):
            showlist = picslist[page*pagesize:(page+1)*pagesize]
        else:
            showlist = picslist[-(totalnum%pagesize+1):-1]
    return jsonify(picslist=showlist,pagesize=pagesize,totalnum=totalnum)

    # time.sleep(2)
    # return jsonify(chapter=chapter.data)





