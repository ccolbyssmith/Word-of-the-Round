$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    socket.on('connect', function() {
        document.getElementById("error").style.display = 'none'
        socket.emit('rejoin_lobby', sessionStorage.getItem('lobbyName'));
        socket.emit('loadPlayerScores', {lobbyName: sessionStorage.getItem('lobbyName')});
        socket.emit('loadInfo', {lobbyName: sessionStorage.getItem('lobbyName')});
        socket.emit('loadChosenPrompt', sessionStorage.getItem('lobbyName'));
        if (sessionStorage.getItem('isJudge') == 'true' || sessionStorage.getItem('submittedAnswer') == 'true') {
            document.getElementById("enterAnswer").style.display = 'none';
        } else if (sessionStorage.getItem('submittedAnswer') != 'true') {
            document.getElementById("Waiting").style.display = 'none';
        }
    });

    socket.on('displayChosenPrompt', function(info) {
        document.getElementById("Prompt").innerHTML = 'Here is your prompt: ' + info['prompt'];
        document.getElementById("Word").innerHTML = 'Here is your word: ' + info['word'];
        sessionStorage.setItem('word', info['word']);
    });

    socket.on('displayPlayerScores', function(players) {
        for (i = 0; i < players.length; i++) {
            if (document.getElementById("playerScores").children[i*2 + 1] == null) {
                var player = document.createElement("player" + i.toString());
                player.id = players[i]['playerID'];
                var text = document.createTextNode(players[i]['playerName'] + ": " + players[i]['score']);
                player.appendChild(text);
                var playerScores = document.getElementById("playerScores");
                linebreak = document.createElement("br");
                playerScores.appendChild(linebreak);
                playerScores.appendChild(player);
            } else {
                var player = document.getElementById(players[i]['playerID']);
                player.innerHTML = players[i] + ": " + players[i]['score'];
            }
        }
    });

    socket.on('getInfo', function(info) {
        document.getElementById('win_data').innerHTML = 'Required Score to Win: ' + info['win_data']
    });

    socket.on('redirect', function(destination) {
        sessionStorage.setItem('submittedAnswer', false)
        console.log('works');
        window.location.href = destination;
        socket.emit('disconnect_request');
    });

    $('form#enterAnswer').submit(function(event) {
        var answer = String(document.getElementById("answer").value.toLowerCase());
        var word = String(sessionStorage.getItem('word').toLowerCase()).replace('\n', '')
        if (answer.includes(word)) {
            document.getElementById("Waiting").style.display = 'block';
            sessionStorage.setItem('submittedAnswer', true);
            socket.emit('logAnswer', {lobbyName: sessionStorage.getItem('lobbyName'), 
                playerId: sessionStorage.getItem('playerId'), answer: answer});
            document.getElementById("enterAnswer").style.display = 'none'
            document.getElementById("Waiting").style.display = 'block'
        } else {
             document.getElementById("error").style.display = 'block'
        }
        return false;
    });

    $('form#leave').submit(function(event) {
        sessionStorage.setItem('gotPrompts', false);
        socket.emit('leaveGame', {lobbyName: sessionStorage.getItem('lobbyName'), 
            playerId: sessionStorage.getItem('playerId')});
        return false;
    });

    socket.on('newHost', function(host) {
        if (host == sessionStorage.getItem('playerId')) {
            sessionStorage.setItem('isHost', true);
        }
    });

    document.getElementById('playerName').innerHTML = sessionStorage.getItem('playerName')
});