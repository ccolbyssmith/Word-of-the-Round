from threading import Lock
from flask import Flask, render_template, session, request, redirect, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import random
import uuid

from .. import socketio
from . import home
from ..models import Player, Lobby, db
thread = None
thread_lock = Lock()

myPlayer = None

#displays the home page (code in home.html)
@home.route('/home')
def displayHomePage():
    return render_template('home.html')

@home.route('/readButton', methods=['POST'])
def readButton():
    urlSuffix = ''
    myLobby = None
    if request.form.get('joinGameButton') == 'joinGame':
        urlSuffix = '/lobby'
        lobbyName = request.form.get('join_room')
        myLobby = Lobby.query.filter_by(name=lobbyName).first()
    elif request.form.get('createGameButton') == 'createGame':
        urlSuffix = '/lobby'
        lobbyName = str(uuid.uuid4()).split('-')[0] 
        myLobby = Lobby(name=lobbyName)
        db.session.add(myLobby)
        db.session.commit()
    if request.form.get('joinGameButton') == 'joinGame' or request.form.get('createGameButton') == 'createGame':
        myPlayer = Player(name=request.form.get('name'), lobby_id=myLobby.id)
        db.session.add(myPlayer)
        db.session.commit()
    prefix = request.path.rsplit('/', 1)[0]
    return redirect(prefix + urlSuffix)

@home.route('/lobby')
def displayLobby():
    return render_template('lobby.html', async_mode=socketio.async_mode)