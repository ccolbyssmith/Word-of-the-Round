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

@game.route('/Phase2')
def displayPhase2():
    return render_template('Game Part2.html');

@game.route('/Phase3')
def displayPhase3():
    return render_template('JudgeChoosingCard.html');

@game.route('/endGame')
def displayEndGame():
    return render_template('End Game.html');