from threading import Lock
from flask import Flask, render_template, session, request, redirect, url_for, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

from .. import socketio
from . import home
from ..models import DataManipulator
thread = None
thread_lock = Lock()
import uuid

dataHelper = DataManipulator()

#maintains the connection between server and user
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1

@socketio.event
def hostLobby(info):
    myPlayerID = str(uuid.uuid4())
    myPlayerName = info['playerName']
    myLobbyName = str(uuid.uuid4()).split('-')[0]
    dataHelper.addLobby(newLobbyName=myLobbyName)
    dataHelper.addPlayer(playerID=myPlayerID, playerName=myPlayerName, lobbyName=myLobbyName)
    destination = url_for('home.displayLobby')
    emit('redirect', {'lobbyName': myLobbyName, 'playerId': myPlayerID, 'playerName': myPlayerName, 
        'destination': destination, 'host': True})

@socketio.event
def joiningLobby(info):
    if dataHelper.lobbyExists(info['lobbyName']) and dataHelper.gameStarted(info['lobbyName']) == False and dataHelper.returnPlayerCount(info['lobbyName']) != 7:
        myPlayerID = str(uuid.uuid4())
        myPlayerName = info['playerName']
        myLobbyName = info['lobbyName']
        dataHelper.addPlayer(playerID=myPlayerID, playerName=myPlayerName, lobbyName=myLobbyName)
        destination = url_for('home.displayLobby')
        emit('redirect', {'lobbyName': myLobbyName, 'playerId': myPlayerID, 'playerName': myPlayerName, 
            'destination': destination, 'host': False})
    else:
        emit('error')
    

#the event invoked to join a lobby
@socketio.event
def join_lobby(message):
    playerID = message['playerId']
    lobbyName = dataHelper.findPlayerLocation(playerID)[0]
    join_room(lobbyName)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('server_response',
         {'data': dataHelper.returnPlayerName(playerID) + ' HAS JOINED THE ROOM'}, to=lobbyName)

#the event invoked to leave a lobby
@socketio.event
def leave(message):
    emit('server_response',
         {'data': dataHelper.returnPlayerName(message['user']) + ' HAS LEFT THE ROOM'}, to=message['lobbyName'])
    leave_room(dataHelper.findPlayerLocation(message['user'])[0])
    destination = url_for('home.displayHomePage')
    dataHelper.deletePlayer(message['user'])
    if dataHelper.returnPlayerCount(message['lobbyName']) == 0:
        dataHelper.deleteLobby(message['lobbyName'])
    else:
        host = dataHelper.getHost(message['lobbyName'])
        emit("newHost", host, to=message['lobbyName'])
    emit('redirect', destination)

#the event invoked to send a message in a lobby
@socketio.event
def my_room_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 
         'user': dataHelper.returnPlayerName(message['user'])},
         to=dataHelper.findPlayerLocation(message['user'])[0])

@socketio.event
def start_game(settings):
    if dataHelper.returnPlayerCount(settings['lobbyName']) >= 3:
        dataHelper.startGame(settings['lobbyName'], settings)
        judge = dataHelper.getJudge(settings['lobbyName'])
        emit('createJudge', judge, to=settings['lobbyName'])
    else:
        emit('failedToStart')

@socketio.event
def gogogo(lobbyName):
    destination = url_for('game.displayPhase1')
    emit('redirect', destination, to=lobbyName)

@socketio.event
def loadNewHost(identification):
    host = dataHelper.getHost(identification['lobbyName'])
    emit('newHost', host, to=identification['lobbyName'])

@socketio.event
def loadPlayerList(identification):
    playerList = dataHelper.loadPlayerList(identification['lobbyName'])
    playerNames = []
    for player in playerList:
        playerNames.append(player['playerName'])
    emit('displayPlayerList', playerNames, to=identification['lobbyName'])

#disconnects user from server
@socketio.event
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('server_response',
         {'data': 'Disconnected!'},
         callback=can_disconnect)

#initaties the connection between the user and the server
@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('server_response', {'data': 'Connected', 'count': 0})