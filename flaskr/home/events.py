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

dataHelper = DataManipulator()

#maintains the connection between server and user
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1

#the event invoked to join a lobby
@socketio.event
def join_lobby(message):
    print('Client Joined Room')
    if message['playerId'] == None:
        playerID = session['myPlayerID']
        lobbyName = session['myLobbyName']
    else:
        playerID = message['playerId']
        lobbyName = dataHelper.findPlayerLocation(playerID)[0]
    join_room(session['myLobbyName'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('server_response',
         {'data': dataHelper.returnPlayerName(playerID) + ' HAS JOINED THE ROOM', 
         'count': session['receive_count']}, to=lobbyName)

#the event invoked to leave a lobby
@socketio.event
def leave(message):
    print('Client Left Room')
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('server_response',
         {'data': dataHelper.returnPlayerName(message['user']) + ' HAS LEFT THE ROOM', 
         'count': session['receive_count']}, to=session['myLobbyName'])
    leave_room(dataHelper.findPlayerLocation(message['user'])[0])
    destination = url_for('home.displayHomePage')
    dataHelper.deletePlayer(session['myPlayerID'])
    if dataHelper.returnPlayerCount(session['myLobbyName']) == 0:
        dataHelper.deleteLobby(session['myLobbyName'])
    emit('redirect', destination)
    session.pop("myLobbyName")
    session.pop('myPlayerID')

#the event invoked to send a message in a lobby
@socketio.event
def my_room_event(message):
    print('message sent')
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count'], 
         'user': dataHelper.returnPlayerName(message['user'])},
         to=dataHelper.findPlayerLocation(message['user'])[0])

@socketio.event
def start_game(settings):
    print('Started Game')
    dataHelper.startGame(settings['lobbyName'], settings)
    destination = url_for('game.displayPhase1')
    emit('redirect', destination, to=settings['lobbyName'])

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
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)

#sends the user's ping
@socketio.event
def my_ping():
    emit('my_pong')

#initaties the connection between the user and the server
@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('server_response', {'data': 'Connected', 'count': 0})

#this is coupled with the disconnect event
@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)