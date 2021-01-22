import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('view', __name__, url_prefix='/Word_of_the_Round')

@bp.route('/home')
def displayHomePage():
    return render_template('home.html')