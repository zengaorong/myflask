from flask import Blueprint

editpu = Blueprint('editpu', __name__)

from . import views
