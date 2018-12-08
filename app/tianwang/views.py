#coding=utf-8
import sys
import uuid
from datetime import  datetime,timedelta
from flask import render_template,request,redirect,url_for,current_app
from . import tianwang
from ..models import Wterror,Watcher,Wtdel
from .. import db
from sqlalchemy import and_


reload(sys)
sys.setdefaultencoding('utf-8')

# 天网故障点位显示
@tianwang.route('/list', methods=['GET'])
def list():
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Wterror,Watcher.watchername,Watcher.id,Watcher.watcherserverip,Watcher.watcherip).outerjoin(Watcher,Watcher.id == Wterror.watcher_id ).filter(Wterror.del_type == 0 ).order_by(Wterror.creat_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items

    listsize = pagination.total

    def get_week_day(date):
        week_day_dict = {
            0 : '星期一',
            1 : '星期二',
            2 : '星期三',
            3 : '星期四',
            4 : '星期五',
            5 : '星期六',
            6 : '星期天',
        }
        day = date.weekday()
        return week_day_dict[day]

    for key in posts:
        key.Wterror.week = get_week_day(key.Wterror.creat_time)
        key.Wterror.creat_time = key.Wterror.creat_time.strftime("%Y-%m-%d %H:%M:%S")

    return render_template('tianwang/list.html',posts=posts,pagination=pagination,listsize=listsize)

# 删除日志
@tianwang.route('/delete',methods=['get'])
def delete():
    id = request.args.get('id', "", type=str)
    wterror = Wterror.query.filter_by(id=id).first()
    wterror.del_type = "1"
    dt = datetime.now()
    time = dt.strftime( '%Y-%m-%d %H:%M:%S' )
    wterror.updata_time = time

    wtdel = Wtdel(id=wterror.id,watcher_id=wterror.watcher_id,creat_time=wterror.creat_time,updata_time=wterror.updata_time,work_for=wterror.work_for,erro_type=wterror.erro_type,log_type=wterror.log_type,del_type=wterror.del_type)

    db.session.add(wtdel)
    db.session.commit()

    db.session.delete(wterror)
    db.session.commit()

    return redirect(url_for('tianwang.list'))

# 故障提交表单
@tianwang.route('/logbook_today',methods=['GET', 'POST'])
def logbook_today():
    id = request.args.get('id', "", type=str)
    wterror = Wterror.query.filter_by(id=id).first()
    return render_template('tianwang/twfrom.html',wterror=wterror)

# 故障保存
@tianwang.route('/savelog', methods=['POST'])
def savelog():
    id = request.form.get('id', "", type=str)
    work_for = request.form.get('work_for', "", type=str)
    if id != "":
        wterror = Wterror.query.filter_by(id=id).first()
        wterror.work_for = work_for

        db.session.add(wterror)
        db.session.commit()
        return redirect(url_for('tianwang.list'))
    return '''<h1>数据错误<h1> <a href="/tianwang/logbook_today?id=%s">返回</a>''' %(id)



@tianwang.route('/list_ys', methods=['GET'])
def list_ys():
    dt = datetime.today().strftime( '%Y-%m-%d' )
    dt = datetime.strptime(dt,'%Y-%m-%d')
    oneday = timedelta(days=1)
    yesterday = dt-oneday
    time = yesterday.strftime( '%Y-%m-%d %H:%M:%S' )
    print time

    # 获取当前时间
    now = datetime.now()
    # 获取今天零点
    zeroToday = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
    # 获取23:59:59
    lastToday = zeroToday - timedelta(hours=23, minutes=59, seconds=59)
    # 获取前一天的当前时间
    yesterdayNow = now - timedelta(hours=23, minutes=59, seconds=59)
    # 获取明天的当前时间
    tomorrowNow = now + timedelta(hours=23, minutes=59, seconds=59)

    # Wtdel.creat_time >= zeroToday and Wtdel.creat_time<=now



    page = request.args.get('page', 1, type=int)

    pagination = db.session.query(Wtdel,Watcher.watchername,Watcher.id,Watcher.watcherserverip,Watcher.watcherip).outerjoin(Watcher,Watcher.id == Wtdel.watcher_id ).filter(and_(Wtdel.updata_time >= lastToday  , Wtdel.updata_time<zeroToday)).order_by(Wtdel.updata_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)

    # pagination = db.session.query(Wtdel).filter(and_(Wtdel.creat_time >= lastToday  , Wtdel.creat_time<now)).order_by(Wtdel.creat_time.desc()).paginate(
    #     page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
    #     error_out=False)
    posts = pagination.items

    listsize = pagination.total

    def get_week_day(date):
        week_day_dict = {
            0 : '星期一',
            1 : '星期二',
            2 : '星期三',
            3 : '星期四',
            4 : '星期五',
            5 : '星期六',
            6 : '星期天',
        }
        day = date.weekday()
        return week_day_dict[day]

    for key in posts:
        key.Wtdel.week = get_week_day(key.Wtdel.creat_time)
        key.Wtdel.creat_time = key.Wtdel.creat_time.strftime("%Y-%m-%d %H:%M:%S")


    return render_template('tianwang/rclist.html',posts=posts,pagination=pagination,listsize=listsize)



@tianwang.route('/test',methods=['GET', 'POST'])
def test():
    return render_template('tianwang/test.html')

