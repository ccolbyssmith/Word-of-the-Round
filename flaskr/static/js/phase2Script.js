$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    socket.on('connect', function() {
        socket.emit('rejoin_lobby', sessionStorage.getItem('lobbyName'));
        socket.emit('loadPlayerScores', {lobbyName: sessionStorage.getItem('lobbyName')});
    });

    $('form#leave').submit(function(event) {
        sessionStorage.setItem('gotPrompts', false);
        socket.emit('leaveGame', {lobbyName: sessionStorage.getItem('lobbyName'), 
            playerId: sessionStorage.getItem('playerId')});
        return false;
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

    document.getElementById('playerName').innerHTML = sessionStorage.getItem('playerName')
});