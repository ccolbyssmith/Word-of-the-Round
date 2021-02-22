from flask import Blueprint

views = Blueprint('views', __name__, url_prefix='/Word_of_the_Round')

from . import homeView, messageView