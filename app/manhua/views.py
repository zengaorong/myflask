#coding=utf-8

from flask import render_template, redirect, request, url_for, flash,jsonify,send_from_directory,\
    current_app
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import manhua
from ..models import Manhua,Chapter
from tools.readexceltool import readexcel_todict
from sqlalchemy import and_
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 漫画首页
@manhua.route('/index',methods=['GET', 'POST'])
def index():
    mhlist = Manhua.query.order_by(Manhua.updata_time.desc()).all()

    if(len(mhlist)>9):
        showlist = mhlist[0:len(mhlist)-1]
    else:
        showlist = mhlist[0:9]
    return render_template('manhua/index.html',mhlist = showlist)


# 漫画章节页面
@manhua.route('/mhchapter/<mh_id>',methods=['GET', 'POST'])
def mhchapter(mh_id):
    chapters = Chapter.query.filter_by(mhname_id = mh_id).order_by(Chapter.chapter_nums.asc()).all()
    manhua = Manhua.query.filter_by(id=mh_id).first()

    page = request.args.get('page', 1, type=int)
    # 使用and__测试联合查询  mhid
    pagination = Chapter.query.filter_by(mhname_id = mh_id).order_by(Chapter.chapter_nums.asc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_CHAP_PAGE'],
        error_out=False)
    posts = pagination.items


    return render_template('manhua/mhchapter.html',manhua=manhua,pagination=pagination,posts=posts)



@manhua.route('/addpic/<chapter_id>')
def addpic(chapter_id):
    return render_template('manhua/showpics.html',chapter_id=chapter_id)

# 前台播放视频功能测试
@manhua.route('/readvideo', methods=['GET', 'POST'])
def readvideo():
    return render_template('manhua/b.html')


# 前台展示全部漫画页面
@manhua.route('/showmhlist', methods=['GET', 'POST'])
def showmhlist():
    mhname = request.args.get('mhname', '', type=str)
    manhua = Manhua.query.filter_by(mhname = mhname ).first()

    # http://127.0.0.1:8083/manhua/mhchapter/c9047140-6928-11e8-a33b-005056c00008
    return redirect(url_for('manhua.mhchapter',mh_id=manhua.id))
    #return render_template('manhua/b.html')


# 根据章节id查询漫画图片路径
@manhua.route('/getpicsbyid',methods=['GET', 'POST'])
def getpics_by_id():
    chapter_id = request.args.get('chapter_id', '', type=str)

    chapter = Chapter.query.filter_by(id = chapter_id).first()
    chapter_strs = chapter.data
    chapter_list = chapter_strs.split('\n')
    print repr(chapter_list[0])
    chapter_list.pop()
    return jsonify(result = chapter_list)


# 测试内部读取excel
@manhua.route('/books', methods=['GET', 'POST'])
def books():
    return render_template('manhua/login.html')

# 测试内部读取excel
@manhua.route('/account', methods=[ 'POST'])
def account():
    account = request.form.get('account')
    password = request.form.get('password')
    dic1 = readexcel_todict("app/manhua/books.xls",1,1,0)
    print dic1[password]
    if(dic1[password][0] == account):
        return "<h1>ok<h1>"
    else:
        return "<h1>wrong<h1>"

# 测试内部读取excel
@manhua.route('/bookadd', methods=['GET', 'POST'])
def bookadd():
    return render_template('manhua/bookadd.html')