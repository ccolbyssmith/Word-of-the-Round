from flask import Flask, render_template, request, redirect
from . import views

#displays the home page (code in home.html)
@views.route('/home')
def displayHomePage():
    return render_template('home.html')

@views.route('/readButton', methods=['POST'])
def readButton():
    urlSuffix = ''
    if request.form.get('joinGameButton') == 'joinGame':
        urlSuffix = '/joinGame'
    elif request.form.get('createGameButton') == 'createGame':
        urlSuffix = '/createGame'
    prefix = request.path.rsplit('/', 1)[0]
    return redirect(prefix + urlSuffix)

@views.route('/joinGame')
def JoinGame():
    return 'Game Joined!'

@views.route('/createGame')
def createGame():
    return 'Game Created!'