from flask import Blueprint

manhua = Blueprint('manhua', __name__)

from . import views