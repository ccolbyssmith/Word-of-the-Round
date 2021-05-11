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

#displays the joinee login page
@home.route('/joineeLoginPage')
def displayHostLoginPage():
    print(session['joinError'])
    return render_template('Joinee Login Page.html')