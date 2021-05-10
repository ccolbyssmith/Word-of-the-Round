from threading import Lock
from flask import Flask, render_template, session, request, redirect, url_for, \
    copy_current_request_context, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import json

from .. import socketio
from . import game
from ..models import DataManipulator
from ..game.gameplay import CardHandler
thread = None
thread_lock = Lock()

dataHelper = DataManipulator()
promptHandler = CardHandler("prompts")
wordHandler = CardHandler("words")

@socketio.event
def rejoin_lobby():
    print('Client Rejoined Room')
    join_room(session['myLobbyName'])
    session['receive_count'] = session.get('receive_count', 0) + 1

@socketio.event
def drawPrompts(info):
    promptHandler.return3Cards(info['lobbyName'])
    prompts = promptHandler.getCurrentCards(info['lobbyName'])
    emit('displayPrompts', prompts, to=info['lobbyName'])

@socketio.event
def loadPrompts(info):
    prompts = promptHandler.getCurrentCards(info['lobbyName'])
    emit('displayPrompts', prompts, to=info['lobbyName'])

@socketio.event
def drawWords(info):
    words = WordHandler.return3Cards()
    wordDict = {'word1': words[0], 'word2': words[1], 'word3': words[2]}
    emit('displayWords', wordDict, to=info['lobbyName'])

@socketio.event
def loadInfo(identification):
    settings = dataHelper.returnSettings(identification['lobbyName'])
    judgeId = dataHelper.getJudge(identification['lobbyName'])
    settings['judgeId'] = judgeId
    emit('getInfo', settings, to=identification['lobbyName'])

@socketio.event
def loadPlayerScores(identification):
    playerList = dataHelper.loadPlayerList(identification['lobbyName'])
    playerNames = []
    for player in playerList:
        playerNames.append(player['playerName'])
    emit('displayPlayerScores', playerNames)

@socketio.event
def leaveGame(info):
    print('Client Left Room')
    session['receive_count'] = session.get('receive_count', 0) + 1
    leave_room(info['lobbyName'])
    destination = url_for('home.displayHomePage')
    dataHelper.deletePlayer(info['playerId'])
    if dataHelper.returnPlayerCount(info['lobbyName']) == 0:
        dataHelper.deleteLobby(info['lobbyName'])
    host = dataHelper.host(info['lobbyName'])
    emit("newHost", host, to=info['lobbyName'])
    emit('redirect', destination)
    session.pop("myLobbyName")
    session.pop('myPlayerID')