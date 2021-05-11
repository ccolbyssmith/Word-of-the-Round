from threading import Lock
from flask import Flask, render_template, session, request, redirect, \
    copy_current_request_context, jsonify, url_for
import json

from .. import socketio
from . import home
from ..models import DataManipulator
import uuid
thread = None
thread_lock = Lock()

data = DataManipulator()

#displays the home page (code in home.html)
@home.route('/home')
def displayHomePage():
    session['joinError'] = False
    return render_template('home.html')

#redirects user to Join a login screen
@home.route('/readHomeButtons', methods=['POST'])
def readHomeButtons():
    urlSuffix = ''
    if request.form.get('joinGameButton') == 'joinGame':
        urlSuffix = '/joineeLoginPage'
    elif request.form.get('createGameButton') == 'createGame':
        urlSuffix = '/hostLoginPage'
    prefix = request.path.rsplit('/', 1)[0]
    return redirect(prefix + urlSuffix)

#displays the lobby page
@home.route('/lobby')
def displayLobby():
    return render_template('lobby.html')

#displays the host login page
@home.route('/hostLoginPage')
def displayLoginPage():
    return render_template('Host Login Page.html')

#redirects the user to a newly generated lobby
@home.route('/readCreateGameButton', methods=['POST'])
def readCreateGameButton():
    urlSuffix = ''
    if request.form.get('yesbuttonlogin') == 'Yes!':
        urlSuffix = '/lobby'
        myPlayerID = str(uuid.uuid4())
        myPlayerName = name=request.form.get('name')
        myLobbyName = str(uuid.uuid4()).split('-')[0]
        data.addLobby(newLobbyName=myLobbyName)
        data.addPlayer(playerID=myPlayerID, playerName=myPlayerName, lobbyName=myLobbyName)
        session['myLobbyName'] = myLobbyName
        session['myPlayerID'] = myPlayerID
    prefix = request.path.rsplit('/', 1)[0]
    return redirect(prefix + urlSuffix) 

#displays the joinee login page
@home.route('/joineeLoginPage')
def displayHostLoginPage():
    print(session['joinError'])
    return render_template('Joinee Login Page.html')

#redirects the user to an already existing lobby
@home.route('/readJoinGameButton', methods=['POST'])
def readJoinGameButton():
    urlSuffix = ''
    if request.form.get('yesbuttonlogin') == 'Yes!':
        myLobbyName = request.form.get('game id')
        if data.lobbyExists(myLobbyName) and data.gameStarted(myLobbyName) == False:
            urlSuffix = '/lobby'
            myPlayerID = str(uuid.uuid4())
            myPlayerName = name=request.form.get('name')
            data.addPlayer(playerID=myPlayerID, playerName=myPlayerName, lobbyName=myLobbyName)
            session['myLobbyName'] = myLobbyName
            session['myPlayerID'] = myPlayerID
        else:
            urlSuffix = '/joineeLoginPage'
            session['joinError'] = True
    prefix = request.path.rsplit('/', 1)[0]
    return redirect(prefix + urlSuffix)
    
#returns playerID and lobbyName for javascript to use
@home.route('/getId', methods=['GET'])
def getdata():
    if request.method == 'GET':
        message = {'myLobbyName': session['myLobbyName'], 'myPlayerID': session['myPlayerID'], 
            'myPlayerName': data.returnPlayerName(session['myPlayerID']), 'host': data.isHost(session['myPlayerID'])}
        return jsonify(message)

@home.route('/getJoinError', methods=['GET'])
def getJoinError():
    if request.method == 'GET':
        message = {'joinError': session['joinError']}
        return jsonify(message)