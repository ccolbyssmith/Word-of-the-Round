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

@home.route('/readHomeButtons', methods=['POST'])
def readHomeButtons():
    urlSuffix = ''
    if request.form.get('joinGameButton') == 'joinGame':
        urlSuffix = '/joineeLoginPage'
    elif request.form.get('createGameButton') == 'createGame':
        urlSuffix = '/hostLoginPage'
    prefix = request.path.rsplit('/', 1)[0]
    return redirect(prefix + urlSuffix)

@home.route('/lobby')
def displayLobby():
    return render_template('lobby.html', async_mode=socketio.async_mode)


@home.route('/hostLoginPage')
def displayLoginPage():
    return render_template('Host Login Page.html')

@home.route('/readCreateGameButton', methods=['POST'])
def readCreateGameButton():
    myPlayer = None
    myLobby = None
    urlSuffix = ''
    if request.form.get('yesbuttonlogin') == 'Yes!':
        urlSuffix = '/lobby'
        myPlayer = Player(name=request.form.get('name'))
        myLobby = Lobby()
        myLobby.addPlayer(myPlayer)
        lobbies.addLobby(newLobby=myLobby)
        session['myLobbyName'] = myLobby.name
        session['myPlayerID'] = myPlayer.id
    prefix = request.path.rsplit('/', 1)[0]
    return redirect(prefix + urlSuffix) 

@home.route('/joineeLoginPage')
def displayHostLoginPage():
    return render_template('Joinee Login Page.html')

@home.route('/readJoinGameButton', methods=['POST'])
def readJoinGameButton():
    myPlayer = None
    myLobby = None
    urlSuffix = ''
    if request.form.get('yesbuttonlogin') == 'Yes!':
        urlSuffix = '/lobby'
        myPlayer = Player(name=request.form.get('name'))
        lobbyName = request.form.get('join_room')
        myLobby = lobbies.findLobby(lobbyName=lobbyName)
        myLobby.addPlayer(myPlayer)
        session['myLobbyName'] = myLobby.name
        session['myPlayerID'] = myPlayer.id
    prefix = request.path.rsplit('/', 1)[0]
    return redirect(prefix + urlSuffix)
    
@home.route('/getData', methods=['GET'])
def getdata():
    if request.method == 'GET':
        message = {'myLobbyName': session['myLobbyName'], 'myPlayerID': session['myPlayerID']}
        return jsonify(message)