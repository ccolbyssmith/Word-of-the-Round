from threading import Lock
from flask import Flask, render_template, session, request, redirect, url_for, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

from .. import socketio
from . import game
from ..models import DataManipulator
thread = None
thread_lock = Lock()

dataHelper = DataManipulator()

@socketio.event
def rejoin_lobby():
    print('Client Rejoined Room')
    join_room(session['myLobbyName'])
    session['receive_count'] = session.get('receive_count', 0) + 1

@socketio.event
def leaveGame():
    print('Client Left Room')
    session['receive_count'] = session.get('receive_count', 0) + 1
    leave_room(session['myLobbyName'])
    destination = url_for('home.displayHomePage')
    dataHelper.deletePlayer(session['myPlayerID'])
    if dataHelper.returnPlayerCount(session['myLobbyName']) == 0:
        dataHelper.deleteLobby(session['myLobbyName'])
    emit('redirect', destination)
    session.pop("myLobbyName")
    session.pop('myPlayerID')