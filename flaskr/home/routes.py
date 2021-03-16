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

def generateLobbyName():
    lobbyname = ''
    for i in range(0, 7):
        randInt = random.randint(0,25)
        if(randInt == 0):
            lobbyname += 'A'
        elif(randInt == 1):
            lobbyname += 'B'
        elif(randInt == 2):
            lobbyname += 'C'
        elif(randInt == 3):
            lobbyname += 'D'
        elif(randInt == 4):
            lobbyname += 'E'
        elif(randInt == 5):
            lobbyname += 'F'
        elif(randInt == 6):
            lobbyname += 'G'
        elif(randInt == 7):
            lobbyname += 'H'
        elif(randInt == 8):
            lobbyname += 'I'
        elif(randInt == 9):
            lobbyname += 'J'
        elif(randInt == 10):
            lobbyname += 'K'
        elif(randInt == 11):
            lobbyname += 'L'
        elif(randInt == 12):
            lobbyname += 'M'
        elif(randInt == 13):
            lobbyname += 'N'
        elif(randInt == 14):
            lobbyname += 'O'
        elif(randInt == 15):
            lobbyname += 'P'
        elif(randInt == 16):
            lobbyname += 'Q'
        elif(randInt == 17):
            lobbyname += 'R'
        elif(randInt == 18):
            lobbyname += 'S'
        elif(randInt == 19):
            lobbyname += 'T'
        elif(randInt == 20):
            lobbyname += 'U'
        elif(randInt == 21):
            lobbyname += 'V'
        elif(randInt == 22):
            lobbyname += 'W'
        elif(randInt == 23):
            lobbyname += 'X'
        elif(randInt == 24):
            lobbyname += 'Y'
        elif(randInt == 25):
            lobbyname += 'Z'
    return lobbyname
