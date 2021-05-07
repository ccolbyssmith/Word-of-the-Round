$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    socket.on('connect', function() {
        socket.emit('rejoin_lobby');
        if (sessionStorage.getItem('isHost') == 'true' && sessionStorage.getItem('gotPrompts') != 'true') {
            sessionStorage.setItem('gotPrompts', true);
            socket.emit('drawPrompts', {lobbyName: sessionStorage.getItem('lobbyName')});
        }
        else {
            socket.emit('loadPrompts', {lobbyName: sessionStorage.getItem('lobbyName')});
        }
    });

    socket.on('redirect', function(destination, cb) {
        console.log('works');
        window.location.href = destination;
        socket.emit('disconnect_request');
        if (cb)
            cb();
    });

    socket.on('displayPrompts', function(prompts) {
        console.log(prompts)
        document.getElementById('Prompt1').innerHTML = prompts['card1'];
        document.getElementById('Prompt2').innerHTML = prompts['card2'];
        document.getElementById('Prompt3').innerHTML = prompts['card3'];
    });

    socket.on('newHost', function(host) {
        if (host == sessionStorage.getItem('playerId')) {
            sessionStorage.setItem('isHost', true);
        }
    });

    $('form#leave').submit(function(event) {
        socket.emit('leaveGame', {lobbyName: sessionStorage.getItem('lobbyName'), 
            playerId: sessionStorage.getItem('playerId')});
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

fetch('/Word_of_the_Round/getJudge')
	.then(response => response.json())
	.then(judgeId => {
		if (sessionStorage.getItem('playerId') != judgeId) {
            document.getElementById('Prompt1').disabled = true;
            document.getElementById('Prompt2').disabled = true;
            document.getElementById('Prompt3').disabled = true;
        }
    });