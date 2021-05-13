from threading import Lock
from flask import Flask, render_template, session, request, redirect, url_for, \
    copy_current_request_context, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import json
import random

from .. import socketio
from . import game
from ..models import DataManipulator
from ..game.gameplay import CardHandler
from ..game.gameplay import AnswerHandler
thread = None
thread_lock = Lock()

dataHelper = DataManipulator()
promptHandler = CardHandler("prompts")
wordHandler = CardHandler("words")
answerHandler = AnswerHandler()

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
    emit('displayPlayerScores', playerList)

@socketio.event
def submitPrompt(info):
    print('phase 2')
    promptHandler.saveChosenCard(info['prompt'], info['lobbyName'])
    wordHandler.saveChosenCard(info['word'], info['lobbyName'])
    destination = url_for('game.displayPhase2')
    emit('redirect', destination, to=info['lobbyName'])

@socketio.event
def loadChosenPrompt(lobbyName):
    chosenPrompt = promptHandler.getChosenCard(lobbyName)
    chosenWord = wordHandler.getChosenCard(lobbyName)
    emit('displayChosenPrompt', {'prompt': chosenPrompt, 'word': chosenWord})

@socketio.event
def logAnswer(info):
    print('phase 3')
    answerHandler.saveAnswer(info['answer'], info['playerId'], info['lobbyName'])
    print(len(answerHandler.getAnswers(info['lobbyName'])))
    print(dataHelper.returnPlayerCount(info['lobbyName']))
    if len(answerHandler.getAnswers(info['lobbyName'])) == dataHelper.returnPlayerCount(info['lobbyName']) - 1:
        destination = url_for('game.displayPhase3')
        emit('redirect', destination, to=info['lobbyName'])

@socketio.event
def loadAnswers(lobbyName):
    answers = answerHandler.getAnswers(lobbyName)
    answerList = list(answers.values())
    for i in range(0, len(answerList)):
        rand = random.randint(0, len(answerList) - 1)
        temp = answerList[i]
        answerList[i] = answerList[rand]
        answerList[rand] = temp
    emit('displayAnswers', answerList)

@socketio.event
def choseAnswer(info):
    winnerOfRoundId = answerHandler.getWinner(info['answer'], info['lobbyName'])
    dataHelper.playerWins(winnerOfRoundId)
    winningPlayer = dataHelper.returnWinningPlayer(info['lobbyName'])
    playerList = dataHelper.loadPlayerList(info['lobbyName'])
    promptHandler.finishRound(info['lobbyName'])
    wordHandler.finishRound(info['lobbyName'])
    answerHandler.finishRound(info['lobbyName'])
    if winningPlayer['score'] == 3:
        destination = url_for('game.displayEndGame')
        emit('redirect', destination, to=info['lobbyName'])
    else:
        dataHelper.newJudge(info['lobbyName'])
        destination = url_for('game.displayPhase1')
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