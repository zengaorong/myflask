#coding=utf-8
from flask import render_template, redirect, request, url_for, flash,jsonify,send_from_directory, \
    current_app
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import spider
from ..models import Manhua,Chapter
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 漫画首页
@spider.route('/leotest',methods=['GET', 'POST'])
def index():
    return render_template('spider/chapter.html')

