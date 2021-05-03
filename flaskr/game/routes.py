from threading import Lock
from flask import Flask, render_template, session, request, redirect, \
    copy_current_request_context, jsonify, url_for
import json

from .. import socketio
from . import game
from ..models import dataManipulator 

data = dataManipulator() 

@game.route('/Phase1')
def displayPhase1():
	isNew = data.lobbyIsNew(session['myLobbyName'])
	return render_template('Game Part1.html')