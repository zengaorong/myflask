#coding=utf-8
import sys
import uuid
from datetime import  datetime
from flask import render_template,request,redirect,url_for,current_app
from . import worker
from ..models import Worker,Logbook
from .. import db
from sqlalchemy import and_


reload(sys)
sys.setdefaultencoding('utf-8')

# 登录界面
@worker.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('worker/login.html')

# 登录验证
@worker.route('/account', methods=[ 'POST'])
def account():
    account = request.form.get('account')
    password = request.form.get('password')
    worker = Worker.query.filter_by(account=account).first()
    if worker!=None and worker.password == password:
        return redirect(url_for('worker.index',workerid=worker.id))
    else:
        return "<h1>账号或者密码不正确，请重新输入<h1>"

# 用户主页
@worker.route('/index/<workerid>',methods=['GET', 'POST'])
def index(workerid):
    worker = Worker.query.filter_by(id=workerid).first()
    return render_template('worker/index.html',worker=worker)


# 生产界面
# 单日日志
@worker.route('/logbook_today',methods=['GET', 'POST'])
def logbook_today():
    workerid = request.args.get('id', "", type=str)
    logbookid = request.args.get('logbookid', "", type=str)
    if logbookid != "":
        logbook = Logbook.query.filter_by(id=logbookid).first()
        logbook.logbook_time = logbook.logbook_time.strftime("%Y-%m-%d")
        return render_template('worker/logbookfrom.html',workerid=workerid,logbook=logbook)
    return render_template('worker/logbookfrom.html',workerid=workerid,logbook=None)

# 保存日志
@worker.route('/savelog', methods=['POST'])
def savelog():
    id = request.form.get('logbookid', "", type=str)
    if id != "":
        work_for = request.form.get('work_for', "", type=str)
        logbook_time = request.form.get('logbook_time', "", type=str)
        logbook = Logbook.query.filter_by(id=id).first()
        if logbook_time!="" and logbook_time != logbook.logbook_time.strftime("%Y-%m-%d"):
            rule = Logbook.logbook_time.like('%' + logbook_time + '%')
            logbook_same = Logbook.query.filter(rule).first()
            if logbook_same:
                return '''<h1>存在该日期的日志，无法修改<h1> <a href="/worker/logbook_today?workerid=%s&logbookid=%s">返回</a>'''%(logbook_same.workerid,id)
            logbook.logbook_time = logbook_time

        # and_(*[Manhua.mhname.like('%' + w + '%') for w in words])
        # rule = and_(*[Logbook.work_for.like('%' + "as" + '%')])
        # logbook = Logbook.query.filter(Logbook.logbook_time.like('%' + "2018-11-17" + '%'))
        # if logbook_time!="" and Logbook.query.filter_by(logbook_time.like(logbook_time))
        dt = datetime.now()
        logbook.updata_time = dt.strftime( '%Y-%m-%d %H:%M:%S' )
        logbook.work_for = work_for
    else:
        work_for = request.form.get('work_for', "", type=str)
        logbook_time = request.form.get('logbook_time', "", type=str)
        log_type = 0
        workerid = request.form.get('id', "", type=str)
        if logbook_time == "":
            return '''<h1>请选择时间<h1>'''

        dt = datetime.now()
        time = dt.strftime( '%Y-%m-%d %H:%M:%S' )
        id = uuid.uuid1()
        logbook = Logbook(id=id,workerid=workerid,logbook_time=logbook_time,work_for=work_for,log_type=log_type,creat_time=time,updata_time=time,)
    db.session.add(logbook)
    db.session.commit()
    return redirect(url_for('worker.loglist',id=logbook.workerid))

# 日志列表 按照时间排序
@worker.route('/loglist', methods=['get'])
def loglist():
    workerid = request.args.get('id', "", type=str)
    page = request.args.get('page', 1, type=int)
    pagination = Logbook.query.filter_by(workerid=workerid).order_by(Logbook.creat_time.desc()).paginate(
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
        key.week = get_week_day(key.logbook_time)
        key.logbook_time = key.logbook_time.strftime("%Y-%m-%d")

    return render_template('worker/loglist.html',posts=posts,pagination=pagination,listsize=listsize,id=workerid)

# 删除日志
@worker.route('/delete',methods=['get'])
def delete():
    id = request.args.get('id', "", type=str)
    logbook = Logbook.query.filter_by(id=id).first()

    db.session.delete(logbook)
    db.session.commit()
    return redirect(url_for('worker.loglist',id=logbook.workerid))

# 管理界面
@worker.route('/workerfrom',methods=['GET', 'POST'])
def workerfrom():
    return render_template('worker/workerfrom.html')


@worker.route('/save', methods=['POST'])
def save():
    account = request.form.get('account', "", type=str)
    password = request.form.get('password', "", type=str)
    workername = request.form.get('workername', "", type=str)
    workerid = uuid.uuid1()
    worker = Worker(id=workerid,account=account,password=password,workername=workername)

    db.session.add(worker)
    db.session.commit()
    return "<h1>%s%s<h1>"%(workername,id)

@worker.route('/test', methods=['POST','get'])
def test():
    return render_template('worker/timetest.html')
