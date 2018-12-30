#coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:7monthdleo@120.79.217.238/spider'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# id 创建时间 发布时间 曲名 别名
# 标题附加信息 专辑（anime） 标签
# 图片路径 介绍 简谱正文 简谱来源链接
# 扒谱人 扒谱人链接 整理着 整理着链接
# 关联演奏 关联歌曲（网易音乐）
class Scores(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    created_time = db.Column(db.DATETIME)
    updated_time = db.Column(db.DATETIME)
    name = db.Column(db.String(255), unique=True)
    alias = db.Column(db.String(64))
    addtion = db.Column(db.String(64))
    anime = db.Column(db.String(255))
    tags = db.Column(db.String(255))
    image_url = db.Column(db.String(128))
    description = db.Column(db.String(255))
    score_text = db.Column(db.Text())
    source_url = db.Column(db.String(128))
    provider = db.Column(db.String(64))
    provider_url = db.Column(db.String(128))
    carrier = db.Column(db.String(64))
    carrier_url = db.Column(db.String(128))
    performs = db.Column(db.String(128))
    songs = db.Column(db.String(255))

    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(64))
    old_url = db.Column(db.String(128))
    # 用户接单 状态变为 进行中 （记录用户id 用户名称）  用户取消 状态变未正常态 用户完成 状态变为完成
    # 初始状态为0 进行为1 完成为2
    opreat_type = db.Column(db.String(1))
    def __repr__(self):
        return '<scores %r>' % self.name

db.create_all()
db.session.commit()