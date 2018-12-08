from flask import Blueprint

worker = Blueprint('worker', __name__)

from . import views