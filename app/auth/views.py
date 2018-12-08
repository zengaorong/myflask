#coding=utf-8
from flask import render_template, redirect, request, url_for, flash,jsonify,send_from_directory
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User,Manhua,Chapter
from ..email import send_email
from .forms import LoginForm, RegistrationForm, Addmhname,UploadForm,photos,fromtest
from sqlalchemy import and_
import os
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
dataname = "leodb"
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/redirect', methods=['GET', 'POST'])
def leo_redirect():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))




@auth.route('/manhuaname', methods=['GET', 'POST'])
def get_manhuaname():
    form = Addmhname()
    if form.validate_on_submit():
        manhua  = Manhua(mhname=form.mhname.data)
        db.session.add(manhua)
        db.session.commit()
    return render_template('auth/addnewmh.html', form=form)
    #return redirect(url_for('auth.leo_redirect'))


@auth.route('/leomahua')
def leomahua():
    list = Manhua.query.order_by(Manhua.mhname)
    return render_template('auth/showmh.html', data_list=list)

@auth.route('/leopic')
def leopic():
    url_list = []
    return render_template('auth/showpic.html', url_list=url_list)


# @auth.route('/add',methods=['GET', 'POST'])
# def add_numbers():
#     chapter_id = request.args.get('chapter_id', '', type=str)
#
#     chapter = Chapter.query.filter_by(id = chapter_id).first()
#     chapter_strs = chapter.data
#     chapter_list = chapter_strs.split('\n')
#     chapter_list.pop()
#     return jsonify(result = chapter_list)


@auth.route('/getindexdata',methods=['GET', 'POST'])
def getindexdata():
    mhlist = Manhua.query.all()
    return jsonify(result = mhlist)




@auth.route('/addpic/<chapter_id>')
def addpic(chapter_id):
    return render_template('auth/showpics.html',chapter_id=chapter_id)


@auth.route('/mhindex',methods=['GET', 'POST'])
def mhindex():
    mhlist = Manhua.query.all()
    return render_template('auth/mhindex.html',mhlist = mhlist)

# @auth.route('/index',methods=['GET', 'POST'])
# def index():
#     mhlist = Manhua.query.all()
#     return render_template('auth/index.html',mhlist = mhlist)


# @auth.route('/mhchapter/<mh_id>',methods=['GET', 'POST'])
# def mhchapter(mh_id):
#     chapters = Chapter.query.filter_by(mhname_id = mh_id).all()
#     return render_template('auth/mhchapter.html',chapters = chapters)



def getDate():
    mhlist = Manhua.query.all()
    for key in  mhlist:
        #print key.mhname
        chapters = Chapter.query.filter_by(mhname_id = key.id).all()
        for chapter in chapters:
            print chapter.chapter_name



    mhname = '火影忍者'
    mh = Manhua.query.filter_by(mhname=mhname).first()
    chapters = Chapter.query.filter_by(mhname_id = mh.id).all()
    chapter_strs = chapters[0].data
    chapter_list = chapter_strs.split('\n')
    chapter_list.pop()
    #return chapter_list



@auth.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.getcwd() + '/app/static/upload',filename)



@auth.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
    else:
        file_url = None
    return render_template('auth/upload.html', form=form, file_url=file_url)



def test3(chaptername,check_str,mhname):
    str_type = check_str.split('.')[-1]
    str_name = chaptername

    pattern = re.compile(u'(.+)\.+(.+)')
    match = pattern.match(check_str)
    str_id =  match.group(1)

    str_nums = str_id.replace(chaptername,'')
    if str_nums.find('num')!=-1:
        str_nums = check_str.split('.')[0].replace('num','')

    return [str_id,str_type,mhname,str_name,str_nums,mhname + '/' + str_name + '/' + check_str]



# http://flask-uploads.readthedocs.io/en/latest/
@auth.route('/uploadImage', methods=['POST'])
def flask_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #logger.debug('No file part')
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            #logger.debug('No selected file')
            return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file'})
        else:
            # try:
                filename = photos.save(file)
                #logger.debug('%s url is %s' % (filename, uploaded_photos.url(filename)))
                return jsonify({'code': 0, 'filename': filename, 'msg': photos.url(filename)})
            # except Exception as e:
            #     #logger.debug('upload file exception: %s' % e)
            #     return jsonify({'code': -1, 'filename': '', 'msg': 'Error occurred'})
    else:
        return jsonify({'code': -1, 'filename': '', 'msg': 'Method not allowed'})


@auth.route('/mhupload',methods=['GET', 'POST'])
def mhupload():
    return render_template('auth/uploadtest.html')


# 修改漫画名称
@auth.route('/showlist', methods=['GET', 'POST'])
def get_showlist():
    mhlist = Manhua.query.all()
    return render_template('auth/from.html',mhlist = mhlist)


@auth.route('/from/<mh_id>', methods=['GET', 'POST'])
def mhfrom(mh_id):
    mhdata = Manhua.query.filter_by(id=mh_id).first()
    leofrom = fromtest()
    if leofrom.validate_on_submit():
        mhdata.mhname = leofrom.mhname.data
        mhdata.pic_url = leofrom.hidden_pic_url.data

        db.session.add(mhdata)
        db.session.commit()
        flash('the profile has been updated')
        return redirect(url_for('auth.get_showlist'))
    leofrom.mhname.data = mhdata.mhname
    leofrom.id.data = mhdata.id
    leofrom.hidden_pic_url.data = mhdata.pic_url
    file_url = mhdata.pic_url
    return render_template('auth/mhfrom.html',mhdata = mhdata,leofrom=leofrom, file_url = file_url)

# @auth.route('/addchapter', methods=['GET', 'POST'])
# def addchapter():
#     mhlist = Manhua.query.all()
#     return render_template('auth/uploadtest.html',mhlist = mhlist)

# @auth.route('/readvideo', methods=['GET', 'POST'])
# def readvideo():
#     return render_template('auth/b.html')


# @auth.route('/manhualist', methods=['GET', 'POST'])
# def manhualist():
#     page = request.args.get('page', 1, type=int)
#     pagination = Manhua.query.order_by(Manhua.id.desc()).paginate(
#         page, per_page=2,
#         error_out=False)
#     posts = pagination.items
#     return render_template('auth/loglist.html',posts=posts,pagination=pagination)


# @auth.route('/wordtest',methods=['GET', 'POST'])
# def wordtest():
#     # chapter_id = request.args.get('chapter_id', '', type=str)
#     #
#     # chapter = Chapter.query.filter_by(id = chapter_id).first()
#     # chapter_strs = chapter.data
#     # chapter_list = chapter_strs.split('\n')
#     # chapter_list.pop()
#
#     words = [request.args.get('mhname', '', type=str)]
#     # words = ['钢']
#     for w in words:
#         print w
#     rule = and_(*[Manhua.mhname.like('%' + w + '%') for w in words])
#     print rule
#     manhua = Manhua.query.filter(rule)
#     chapter_list =  ['测试','测试1']
#     for key in manhua:
#         chapter_list.append(key.mhname)
#
#     return jsonify(result = chapter_list)