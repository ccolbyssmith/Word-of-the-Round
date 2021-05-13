$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();
    
    socket.on('connect', function() {
        socket.emit('rejoin_lobby', sessionStorage.getItem('lobbyName'));
        socket.emit('loadPlayerScores', {lobbyName: sessionStorage.getItem('lobbyName')});
        socket.emit('loadWinningStatus', {lobbyName: sessionStorage.getItem('lobbyName'), playerId: sessionStorage.getItem('playerId')});
        if (sessionStorage.getItem('isHost') != 'true') {
            document.getElementById('return').style.display = 'none'
        }
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

    socket.on('redirect', function(destination) {
        window.location.href = destination;
        socket.emit('disconnect_request');
    });

    socket.on('displayPlacement', function(info) {
        if (info['winner'] == true) {
            document.getElementById("heading").innerHTML = 'YOU WIN!'
        } else {
            document.getElementById("heading").innerHTML = 'YOU LOSE!'
        }
    });

    $('form#return').submit(function(event) {
        socket.emit('returnToMenu', sessionStorage.getItem('lobbyName'));
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