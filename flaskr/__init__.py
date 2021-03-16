import os

from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()
app = Flask(__name__)
from .models import LobbyList
lobbies = LobbyList()

def create_app(debug=False):
    """Create an application."""
    app.config['TESTING'] = True
    app.debug = debug
    from .home import home as home
    app.register_blueprint(home)
    socketio.init_app(app)
    return app