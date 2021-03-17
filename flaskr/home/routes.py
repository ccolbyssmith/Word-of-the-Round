from threading import Lock
from flask import Flask, render_template, session, request, redirect, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import json

from .. import socketio
from . import home
from ..models import Lobby, Player
from ..__init__ import lobbies
thread = None
thread_lock = Lock()

#displays the home page (code in home.html)
@home.route('/home')
def displayHomePage():
    return render_template('home.html')

@home.route('/readButton', methods=['POST'])
def readButton():
    myPlayer = None
    myLobby = None
    urlSuffix = ''
    if request.form.get('joinGameButton') == 'joinGame':
        urlSuffix = '/readButton'
        lobbyName = request.form.get('join_room')
        myLobby = lobbies.findLobby(lobbyName=lobbyName)
    elif request.form.get('createGameButton') == 'createGame':
        urlSuffix = '/readButton'
        myLobby = Lobby()
        lobbies.addLobby(newLobby=myLobby)
    if request.form.get('joinGameButton') == 'joinGame' or request.form.get('createGameButton') == 'createGame':
        myPlayer = Player(name=request.form.get('name'))
        lobbies.findLobby(lobbyName=myLobby.name).addPlayer(player=myPlayer)
    prefix = request.path.rsplit('/', 1)[0]
    session['myLobbyName'] = myLobby.name
    session['myPlayerID'] = myPlayer.id
    return redirect(prefix + urlSuffix)

@home.route('/lobby')
def displayLobby():
    return render_template('lobby.html', async_mode=socketio.async_mode, 
        myLobbyName=json.dumps(session.get('myLobbyName', None)), myPlayerID=json.dumps(session.get('myPlayerID', None)))