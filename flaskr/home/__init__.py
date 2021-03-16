from flask import Blueprint

home = Blueprint('home', __name__, url_prefix='/Word_of_the_Round')

from . import routes, events