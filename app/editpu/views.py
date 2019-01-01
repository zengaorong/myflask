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
import sys

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
