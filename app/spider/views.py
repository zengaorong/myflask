#coding=utf-8
from flask import render_template, redirect, request, url_for, flash,jsonify,send_from_directory, \
    current_app
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import spider
from serch import get_serch_list
from app.leotool.bs64pic.pic_to_bs64 import get_picbase64
from ..models import Manhua,Chapter
from .form import fromtest
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 漫画首页
@spider.route('/leotest',methods=['GET', 'POST'])
def index():
    return render_template('spider/loading.html')

# ajax
@spider.route('/ajax/index',methods=['GET', 'POST'])
def ajax_index():
    return jsonify(result="ok")

@spider.route('/search/story',methods=['GET', 'POST'])
def search_story():
    serch_str = "元尊"
    serch_list = get_serch_list(serch_str)
    print len(serch_list)
    imagebase64 = get_picbase64("app/leotool/bs64pic/chaotian.jpg")
    return render_template('spider/story_list.html',serch_list=serch_list,imagebase64=imagebase64)


@spider.route('/register', methods=['GET', 'POST'])
def register():
    form = fromtest()
    #
    # if form.validate_on_submit():
    #     return "sucsses"
    #     # user = User(email=form.email.data,
    #     #             username=form.username.data,
    #     #             password=form.password.data)
    #     # db.session.add(user)
    #     # db.session.commit()
    #     # addr = current_app.config['FLASKY_SERTVER_ADDR']
    #     # token = user.generate_confirmation_token()
    #     # send_email(user.email, 'Confirm Your Account',
    #     #            'auth/email/confirm', user=user, token=token ,addr=addr)
    #     # flash('A confirmation email has been sent to you by email.')
    #     # return redirect(url_for('auth.login'))
    # # return form
    return render_template('spider/ajaxsubmit.html',form=form)


@spider.route('/submit', methods=['GET', 'POST'])
def submit():
    email = request.form.get("email")
    print email
    return jsonify(True)

