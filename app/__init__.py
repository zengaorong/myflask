from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
photos = UploadSet('photos', IMAGES)

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    configure_uploads(app, photos)
    patch_request_class(app)  # set maximum file size, default is 16MB

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .mhcontrol import mhcontrol as mhcontrol_blueprint
    app.register_blueprint(mhcontrol_blueprint, url_prefix='/mhcontrol')

    from .manhua import manhua as manhu_blueprint
    app.register_blueprint(manhu_blueprint, url_prefix='/manhua')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .chaptercontrol import chaptercontrol as chaptercontrol_blueprint
    app.register_blueprint(chaptercontrol_blueprint, url_prefix='/chaptercontrol')

    from .worker import worker  as worker_blueprint
    app.register_blueprint(worker_blueprint, url_prefix='/worker')

    from .tianwang import tianwang  as tianwang_blueprint
    app.register_blueprint(tianwang_blueprint, url_prefix='/tianwang')

    return app
