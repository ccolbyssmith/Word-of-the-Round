import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()
app = Flask(__name__)

db = SQLAlchemy()

def create_app(debug=False):
    """Create an application."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db.init_app(app)
    app.debug = debug
    from .home import home as home
    app.register_blueprint(home)
    socketio.init_app(app)
    return app