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
def rejoin_lobby(lobbyName):
    print('Client Rejoined Room')
    join_room(lobbyName)
    session['receive_count'] = session.get('receive_count', 0) + 1

@socketio.event
def drawPrompts(info):
    promptHandler.return3Cards(info['lobbyName'])
    wordHandler.return3Cards(info['lobbyName'])
    emit('drewPrompts', to=info['lobbyName'])

@socketio.event
def loadPrompts(info):
    currentPrompts = promptHandler.getCurrentCards(info['lobbyName'])
    prompts = {}
    prompts['prompt1'] = currentPrompts['card1']
    prompts['prompt2'] = currentPrompts['card2']
    prompts['prompt3'] = currentPrompts['card3']
    currentWords = wordHandler.getCurrentCards(info['lobbyName'])
    prompts['word1'] = currentWords['card1']
    prompts['word2'] = currentWords['card2']
    prompts['word3'] = currentWords['card3']
    emit('displayPrompts', prompts)

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
def submitPrompt(info):
    print('phase 2')
    promptHandler.saveChosenCard(info['prompt'], info['lobbyName'])
    wordHandler.saveChosenCard(info['word'], info['lobbyName'])
    destination = url_for('game.displayPhase2')
    emit('redirect', destination, to=info['lobbyName'])

@socketio.event
def leaveGame(info):
    print('Client Left Room')
    session['receive_count'] = session.get('receive_count', 0) + 1
    leave_room(info['lobbyName'])
    destination = url_for('home.displayHomePage')
    dataHelper.deletePlayer(info['playerId'])
    if dataHelper.returnPlayerCount(info['lobbyName']) == 0:
        dataHelper.deleteLobby(info['lobbyName'])
    else:
        host = dataHelper.getHost(info['lobbyName'])
        emit("newHost", host, to=info['lobbyName'])
    emit('redirect', destination)