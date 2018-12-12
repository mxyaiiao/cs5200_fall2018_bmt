from flask import Blueprint

noticer = Blueprint('noticer', __name__)

from . import views
