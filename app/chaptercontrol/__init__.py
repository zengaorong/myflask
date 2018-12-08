from flask import Blueprint

chaptercontrol = Blueprint('chaptercontrol', __name__)

from . import views