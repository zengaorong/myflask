from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:7monthdleo@127.0.0.1/leodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Watcher(db.Model):
    __tablename__ = 'watcher'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    watchernum = db.Column(db.VARCHAR(5))
    watchername = db.Column(db.String(64))
    watchertown = db.Column(db.String(5))
    watchertype = db.Column(db.String(5))
    watcherserverip = db.Column(db.String(64))
    watcherip = db.Column(db.String(64))
    watcherlongitude = db.Column(db.DECIMAL(10,6))
    watcherlatitude = db.Column(db.DECIMAL(10,6))
    account = db.Column(db.VARCHAR(36))
    password = db.Column(db.VARCHAR(36))
    def __repr__(self):
        return '<Watcher %r>' % self.watchername

class Wterror(db.Model):
    __tablename__ = 'wterror'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    watcher_id = db.Column(db.VARCHAR(36),db.ForeignKey('watcher.id'))
    creat_time = db.Column(db.DATETIME)
    updata_time = db.Column(db.DATETIME)
    work_for = db.Column(db.String(1024))
    erro_type = db.Column(db.VARCHAR(5))
    log_type = db.Column(db.VARCHAR(1))
    del_type = db.Column(db.VARCHAR(1))
    def __repr__(self):
        return '<Watcher %r>' % self.watchername

class Wtdel(db.Model):
    __tablename__ = 'wtdel'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    watcher_id = db.Column(db.VARCHAR(36),db.ForeignKey('watcher.id'))
    creat_time = db.Column(db.DATETIME)
    updata_time = db.Column(db.DATETIME)
    work_for = db.Column(db.String(1024))
    erro_type = db.Column(db.VARCHAR(5))
    log_type = db.Column(db.VARCHAR(1))
    del_type = db.Column(db.VARCHAR(1))
    def __repr__(self):
        return '<Watcher %r>' % self.watchername

#  物资使用情况表 材料类别（光分插片 服务器 光猫 球机 电缆） （更换） 该表对应故障表 使用故障条目的时间  修复描述 说明
class Wtdel(db.Model):
    __tablename__ = 'wtdel'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    watcher_id = db.Column(db.VARCHAR(36),db.ForeignKey('watcher.id'))
    creat_time = db.Column(db.DATETIME)
    updata_time = db.Column(db.DATETIME)
    work_for = db.Column(db.String(1024))
    erro_type = db.Column(db.VARCHAR(5))
    log_type = db.Column(db.VARCHAR(1))
    del_type = db.Column(db.VARCHAR(1))
    def __repr__(self):
        return '<Watcher %r>' % self.watchername

db.create_all()
db.session.commit()