from flask import Blueprint

home = Blueprint('game', __name__, url_prefix='/Word_of_the_Round')

from . import routes, events