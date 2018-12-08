from flask import Blueprint

mhcontrol = Blueprint('mhcontrol', __name__)

from . import views