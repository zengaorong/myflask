#coding=utf-8

from flask import render_template, redirect, request, url_for, flash,jsonify,send_from_directory,\
    current_app
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import mhcontrol
from ..models import Manhua,Chapter
from sqlalchemy import and_
from datetime import  datetime
import uuid
from .forms import fromtest
from .. import db
import sys
import urllib
import os
import platform,shutil

reload(sys)
sys.setdefaultencoding('utf-8')

# 测试路径使用
@mhcontrol.route('/index')
def index():
    print current_app
    print current_app.config['FLASKY_POSTS_PER_PAGE']
    return render_template('mhcontrol/index.html',data='control')


# 漫画名称模糊查询的ajax后台代码 这个可以归属于公共类中 访问者和管理员都能使用
@mhcontrol.route('/getmhname',methods=['GET', 'POST'])
def getmhname():
    words = [request.args.get('mhname', '', type=str)]
    for w in words:
        print w
    rule = and_(*[Manhua.mhname.like('%' + w + '%') for w in words])
    print rule
    manhua = Manhua.query.filter(rule)
    chapter_list =  ['测试','测试1']
    for key in manhua:
        chapter_list.append(key.mhname)
    return jsonify(result = chapter_list)


# 后台展示漫画的列表 这里的列表构建需要再研究下
@mhcontrol.route('/manhualist', methods=['GET', 'POST'])
def manhualist():
    page = request.args.get('page', 1, type=int)
    pagination = Manhua.query.order_by(Manhua.updata_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items

    listsize = pagination.total
    return render_template('mhcontrol/list.html',posts=posts,pagination=pagination,listsize=listsize)


@mhcontrol.route('/delete',methods=['get'])
def delete():
    id = request.args.get('id', "", type=str)
    manhua = Manhua.query.filter_by(id=id).first()
    chapterlist = Chapter.query.filter_by(mhname_id = id)
    for key in chapterlist:
        print key

        if(key.data==None):
            db.session.delete(key)
            db.session.commit()

        else:
            pic_list = key.data.split('\n')
            chaptername = key.chapter_name
            mhname = manhua.mhname


            cwd = os.getcwd()
            dir = '/app/static/pics/'
            test_str = (cwd + '/app/static/pics/' + mhname + '/' + chaptername)

            if(platform.system()=='Windows'):
                test_str = test_str.replace("\\",'/')

            if(os.path.exists(test_str)):
                shutil.rmtree(test_str)
            db.session.delete(key)
            db.session.commit()

    cwd = os.getcwd()
    mhname = manhua.mhname
    test_str = (cwd + '/app/static/pics/' + mhname )
    shutil.rmtree(test_str)
    db.session.delete(manhua)
    db.session.commit()
    return redirect(url_for('mhcontrol.manhualist'))


# 后台添加漫画 查询漫画名称 并选择名称添加漫画
@mhcontrol.route('/uploadmanhuapics', methods=['GET', 'POST'])
def upload_manhua_pics():
    return render_template('mhcontrol/mhfrom.html')


# 后台修改漫画 准备和添加合并 毕竟如果没有id就是新建
@mhcontrol.route('/backfrom', methods=['GET', 'POST'])
def backfrom():
    id = request.args.get('id', "", type=str)
    picsname = None
    if(id!=""):
        manhua = Manhua.query.filter_by(id=id).first()
        if(manhua.pic_url!=""and manhua.pic_url!=None):
            picsname = manhua.pic_url.split('/')[-1]
        picsname = urllib.unquote(str(picsname))
    else:
        manhua = Manhua(id=None,mhname="",pic_base64data="",)
    return render_template('mhcontrol/backfrom.html',manhua=manhua,picsname=picsname)


# 后台修改漫画 准备和添加合并 毕竟如果没有id就是新建
@mhcontrol.route('/save', methods=['POST'])
def save():
    mhname = request.form.get('mhname', "", type=str)
    id = request.form.get('mhid', "", type=str)
    mhurl = request.form.get('mhurl', "", type=str)
    base64data = request.form.get('base64data', "", type=str)
    if(id!="" and id!='None'):
        manhua = Manhua.query.filter_by(id=id).first()
        dt = datetime.now()
        manhua.updata_time = dt.strftime( '%Y-%m-%d %H:%M:%S' )
        manhua.mhname = mhname
        manhua.pic_base64data = base64data
        manhua.pic_url = mhurl
    else:
        dt = datetime.now()
        time = dt.strftime( '%Y-%m-%d %H:%M:%S' )
        id = uuid.uuid1()
        manhua = Manhua(id=id,mhname=mhname,creat_time=time,updata_time=time,pic_base64data = base64data,pic_url = mhurl)

    db.session.add(manhua)
    db.session.commit()
    return redirect(url_for('mhcontrol.manhualist'))

# # 漫画后台主页 目前是manhualist进入管理页面
# @mhcontrol.route('/main', methods=['GET', 'POST'])
# def main():
#     return render_template('mhcontrol/main.html')




