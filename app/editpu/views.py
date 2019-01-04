#coding=utf-8
from flask import render_template, redirect, request, url_for, flash,jsonify,send_from_directory, \
    current_app
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import editpu
from .. import db
from sqlalchemy import and_
from form import details_qupu,select_list
from app.leotool.bs64pic.pic_to_bs64 import get_picbase64
from ..models import Scores
from data.operatedb import check_qupu_name_todb,insert_qupu_todb
from datetime import datetime
import sys
import xlrd
import uuid

reload(sys)
sys.setdefaultencoding('utf-8')

# 曲谱主页
@editpu.route('/index',methods=['GET', 'POST'])
def index():
    return "ok"


# 曲谱领区任务主页
@editpu.route('/list', methods=['GET','post'])
@login_required
def list():
    # 检测是否带参数
    qu_name = request.form.get('qu_name', "", type=str)
    pagination_qu_name = request.args.get('qu_name', "", type=str)
    # 存在搜索参数
    if qu_name!="" or pagination_qu_name!="":
        form = select_list()
        if qu_name!="":
            pagination_qu_name = qu_name
        form.qu_name.data = pagination_qu_name
        page = request.args.get('page', 1, type=int)
        pagination = db.session.query(Scores.id,Scores.old_url,Scores.name,Scores.opreat_type,Scores.provider,Scores.user_name).filter(Scores.opreat_type!=2 , Scores.name.like('%' + pagination_qu_name + '%')).order_by(Scores.created_time.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        posts = pagination.items
        listsize = pagination.total
        return render_template('editpu/list.html',posts=posts,pagination=pagination,listsize=listsize,form=form,qu_name=pagination_qu_name)


    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Scores.id,Scores.old_url,Scores.name,Scores.opreat_type,Scores.provider,Scores.user_name).filter(Scores.opreat_type!=2).order_by(Scores.created_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    listsize = pagination.total

    form = select_list()
    return render_template('editpu/list.html',posts=posts,pagination=pagination,listsize=listsize,form=form)


# 曲谱详情
@editpu.route('/details', methods=['GET'])
def details():
    id = request.args.get('id', "", type=int)
    if id != "":
        scores = Scores.query.filter_by(id=id).first()
        form = details_qupu()
        form.id.data = id
        form.title.data = scores.name
        form.jianpu.data = scores.score_text
        form.oldurl.data = scores.old_url
        return render_template('editpu/details.html',form=form)
    return '''<h1>数据错误,联系吉吉米米解决<h1> <a href="/editpu/list">返回</a>'''

# 领取任务
@editpu.route('/gettask', methods=['post'])
@login_required
def gettask():
    id = request.form.get('qupu_id', "", type=int)
    if id != "":
        scores = Scores.query.filter_by(id=id).first()
        scores.user_id = current_user.id
        scores.user_name = current_user.username
        scores.opreat_type = "1"
        db.session.add(scores)
        db.session.commit()
        return jsonify(data=True)
    return '''<h1>数据错误,联系吉吉米米解决<h1> <a href="/editpu/list">返回</a>'''

# 登出
@editpu.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('editpu.list'))

# 放弃任务
@editpu.route('/giveuptask')
@login_required
def giveuptask():
    id = request.args.get('id', "", type=int)
    if id != "":
        scores = Scores.query.filter_by(id=id).first()
        scores.user_id = None
        scores.user_name = None
        scores.opreat_type = "0"
        db.session.add(scores)
        db.session.commit()
        return redirect(url_for('editpu.personlist'))
    return '''<h1>数据错误,联系吉吉米米解决<h1> <a href="/editpu/list">返回</a>'''


# giveuptask
# 登出
@editpu.route('/overtask')
@login_required
def overtask():
    id = request.args.get('id', "", type=int)
    if id != "":
        scores = Scores.query.filter_by(id=id).first()
        scores.opreat_type = "2"
        db.session.add(scores)
        db.session.commit()
        return redirect(url_for('editpu.personoverlist'))
    return '''<h1>数据错误,联系吉吉米米解决<h1> <a href="/editpu/list">返回</a>'''

# 个人任务列表
@editpu.route('/personlist', methods=['GET','post'])
@login_required
def personlist():
    # 检测是否带参数
    qu_name = request.form.get('qu_name', "", type=str)
    pagination_qu_name = request.args.get('qu_name', "", type=str)
    # 存在搜索参数
    if qu_name!="" or pagination_qu_name!="":
        form = select_list()
        if qu_name!="":
            pagination_qu_name = qu_name
        form.qu_name.data = pagination_qu_name
        page = request.args.get('page', 1, type=int)
        pagination = db.session.query(Scores.id,Scores.name,Scores.opreat_type,Scores.provider,Scores.user_name).filter(and_(Scores.opreat_type!="2" , Scores.user_id == current_user.id , Scores.name.like('%' + pagination_qu_name + '%'))).order_by(Scores.created_time.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        posts = pagination.items
        listsize = pagination.total
        return render_template('editpu/personlist.html',posts=posts,pagination=pagination,listsize=listsize,form=form,qu_name=pagination_qu_name)


    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Scores.id,Scores.name,Scores.opreat_type,Scores.provider,Scores.user_name).filter(Scores.opreat_type!="2" , Scores.user_id == current_user.id).order_by(Scores.created_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    listsize = pagination.total


    form = select_list()
    return render_template('editpu/personlist.html',posts=posts,pagination=pagination,listsize=listsize,form=form)


# 个人完成列表
@editpu.route('/personoverlist', methods=['GET','post'])
@login_required
def personoverlist():
    # 检测是否带参数
    qu_name = request.form.get('qu_name', "", type=str)
    pagination_qu_name = request.args.get('qu_name', "", type=str)
    # 存在搜索参数
    if qu_name!="" or pagination_qu_name!="":
        form = select_list()
        if qu_name!="":
            pagination_qu_name = qu_name
        form.qu_name.data = pagination_qu_name
        page = request.args.get('page', 1, type=int)
        pagination = db.session.query(Scores.id,Scores.name,Scores.opreat_type,Scores.provider,Scores.user_name).filter(and_(Scores.opreat_type==2 , Scores.user_id == current_user.id , Scores.name.like('%' + pagination_qu_name + '%'))).order_by(Scores.created_time.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        posts = pagination.items
        listsize = pagination.total
        return render_template('editpu/personlist.html',posts=posts,pagination=pagination,listsize=listsize,form=form,qu_name=pagination_qu_name)


    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Scores.id,Scores.name,Scores.opreat_type,Scores.provider,Scores.user_name).filter(Scores.opreat_type==2 , Scores.user_id == current_user.id).order_by(Scores.created_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    listsize = pagination.total

    form = select_list()
    return render_template('editpu/personoverlist.html',posts=posts,pagination=pagination,listsize=listsize,form=form)


# 完成列表
@editpu.route('/overlist', methods=['GET','post'])
@login_required
def overlist():
    # 检测是否带参数
    qu_name = request.form.get('qu_name', "", type=str)
    pagination_qu_name = request.args.get('qu_name', "", type=str)
    # 存在搜索参数
    if qu_name!="" or pagination_qu_name!="":
        form = select_list()
        if qu_name!="":
            pagination_qu_name = qu_name
        form.qu_name.data = pagination_qu_name
        page = request.args.get('page', 1, type=int)
        pagination = db.session.query(Scores.id,Scores.name,Scores.opreat_type,Scores.provider,Scores.user_name).filter(and_(Scores.opreat_type==2 , Scores.name.like('%' + pagination_qu_name + '%'))).order_by(Scores.created_time.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        posts = pagination.items
        listsize = pagination.total
        return render_template('editpu/overlist.html',posts=posts,pagination=pagination,listsize=listsize,form=form,qu_name=pagination_qu_name)


    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Scores.id,Scores.name,Scores.opreat_type,Scores.provider,Scores.user_name).filter(Scores.opreat_type==2 ).order_by(Scores.created_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    listsize = pagination.total

    form = select_list()
    return render_template('editpu/overlist.html',posts=posts,pagination=pagination,listsize=listsize,form=form)



# 完成列表
@editpu.route('/complexselect', methods=['GET','post'])
@login_required
def complexselect():
    qupu_list = request.form.getlist('qupu_ids[]')
    for id in qupu_list:
        scores = Scores.query.filter_by(id=id).first()
        if scores.user_id=="" or scores.user_id==None:
            scores.user_id = current_user.id
            scores.user_name = current_user.username
            scores.opreat_type = 1
            db.session.add(scores)
            db.session.commit()
        else:
            continue
    return jsonify(data="ok")

from flask import send_from_directory
from werkzeug.utils import secure_filename
@editpu.route('/get_attachment/<path:filename>')
def get_attachment(filename):
    print filename
    return send_from_directory(current_app.config['UPLOADED_PHOTOS_DEST'],filename,as_attachment=True)


ALLOWED_EXTENSIONS = ['xls', 'xlsx']

def allowe_file(filename):
    '''
    限制上传的文件格式
    :param filename:
    :return:
    '''
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


@editpu.route('/upload', methods=['GET', 'POST'])
@login_required
def updata():
    return render_template('editpu/upload.html')

import os
import uuid
@editpu.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    # file = request.files.get('文件名') # 获取文件
    file = request.files['file']
    filename = secure_filename(file.filename)  # 获取文件名
    #file.save(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)) # 保存文件
    excel_dict = {}
    try:
        f = file.read()    #文件内容
        excel_workbook = xlrd.open_workbook(file_contents=f)
        excel_sheet01 = excel_workbook.sheets()[0]
        terminal_num_nrows = excel_sheet01.nrows
        terminal_num_ncols = excel_sheet01.ncols

        for r in range(1,terminal_num_nrows):
            key_str = excel_sheet01.cell(r,0).value
            hold = []
            #print int(key_str)
            for c in range(0,terminal_num_ncols):
                if type(excel_sheet01.cell(r,c).value) is float:
                    hold.append(str((excel_sheet01.cell(r,c).value)))
                else:
                    hold.append(excel_sheet01.cell(r,c).value)
            # 存入字典中
            excel_dict[key_str] =  hold
    except:
        return "上传格式不正确"

    success_list = []
    error_list = []
    for key in excel_dict:
        if check_qupu_name_todb(key):
            error_list.append(key)
        else:
            insert_list = [uuid.uuid1(),datetime.now(),key,excel_dict[key][1],None,None,None,None,0,]
            insert_qupu_todb(insert_list)
            success_list.append(key)

    return render_template('editpu/uploadtips.html',error_list=error_list)

    # if request.method == 'POST':
    #     file = request.files['file']
    #     if file and allowe_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    #         old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    #         new_filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1]
    #         new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    #         os.rename(old_path, new_path)
    #
    #         return 'ok'
    #
    # return 'not ok'