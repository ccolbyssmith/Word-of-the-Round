$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    socket.on('connect', function() {
        socket.emit('rejoin_lobby');
    });

    socket.on('redirect', function(destination, cb) {
        console.log('works')
        window.location.href = destination;
        socket.emit('disconnect_request');
        if (cb)
            cb();
    });

    $('form#leave').submit(function(event) {
        socket.emit('leaveGame');
        return false;
    });
});

fetch('/Word_of_the_Round/getPlayers')
	.then(response => response.json())
	.then(players => {
        console.log(players);
        for (i = 0; i < players.length; i++) {
            var player = document.createElement("player" + i.toString());
            var text = document.createTextNode(players[i] + ": 0");
            player.appendChild(text);
            var playerScores = document.getElementById("playerScores");
            linebreak = document.createElement("br");
            playerScores.appendChild(linebreak);
            playerScores.appendChild(player);
        }
    });