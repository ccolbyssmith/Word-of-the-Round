import os

from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()
app = Flask(__name__)
from .models import dataManipulator

def create_app(debug=False):
    data = dataManipulator()
    data.createNewData()
    """Create an application."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'This is a Secret'
    app.debug = debug
    from .home import home as home
    app.register_blueprint(home)
    socketio.init_app(app)
    return app