from threading import Lock
from flask import Flask, render_template, session, request, redirect, \
    copy_current_request_context, jsonify, url_for
import json

from .. import socketio
from . import game
from ..models import DataManipulator
from ..game.gameplay import CardHandler

dataHelper = DataManipulator()
promptHandler = CardHandler("prompts")
wordHandler = CardHandler("words")

@game.route('/Phase1')
def displayPhase1():
    return render_template('Game Part1.html');

@game.route('/getSettings', methods=['GET'])
def getSettings():
    if request.method == 'GET':
        message = dataHelper.returnSettings(session['myLobbyName'])
        return jsonify(message)

@game.route('/getJudge', methods=['GET'])
def getJudge():
    if request.method == 'GET':
        judgeId = dataHelper.getJudge(session['myLobbyName'])
        return jsonify(judgeId)