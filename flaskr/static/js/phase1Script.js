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
        socket.emit('loadInfo', {lobbyName: sessionStorage.getItem('lobbyName')});
        socket.emit('loadPlayerScores', {lobbyName: sessionStorage.getItem('lobbyName')});
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
        document.getElementById('Prompt1').innerHTML = prompts['prompt1'];
        document.getElementById('Prompt2').innerHTML = prompts['prompt2'];
        document.getElementById('Prompt3').innerHTML = prompts['prompt3'];
        document.getElementById('Word1').innerHTML = prompts['word1'];
        document.getElementById('Word2').innerHTML = prompts['word2'];
        document.getElementById('Word3').innerHTML = prompts['word3'];
    });

    socket.on('displayPlayerScores', function(players) {
        for (i = 0; i < players.length; i++) {
            if (document.getElementById("playerScores").children[i + 1] == null) {
                var player = document.createElement("player" + i.toString());
                player.id = players[i]
                var text = document.createTextNode(players[i] + ": 0");
                player.appendChild(text);
                var playerScores = document.getElementById("playerScores");
                linebreak = document.createElement("br");
                playerScores.appendChild(linebreak);
                playerScores.appendChild(player);
            } else {
                var player = document.getElementById(players[i]);
                player.innerHTML = players[i] + ": 0"
            }
        }
    });

    socket.on('newHost', function(host) {
        if (host == sessionStorage.getItem('playerId')) {
            sessionStorage.setItem('isHost', true);
        }
    });

    socket.on('getInfo', function(info) {
        if (sessionStorage.getItem('playerId') != info['judgeId']) {
            document.getElementById('Prompt1').disabled = true;
            document.getElementById('Prompt2').disabled = true;
            document.getElementById('Prompt3').disabled = true;
        }
    });

    $('form#leave').submit(function(event) {
        sessionStorage.setItem('gotPrompts', false);
        socket.emit('leaveGame', {lobbyName: sessionStorage.getItem('lobbyName'), 
            playerId: sessionStorage.getItem('playerId')});
        return false;
    });

    $('form#submitPrompt').submit(function(event) {
        var promptButtonId;
        var wordButtonId;
        if (document.getElementById('prompt1Mark').checked) {
            promptButtonId = document.getElementById('prompt1Mark').value;
        } else if (document.getElementById('prompt2Mark').checked) {
            promptButtonId = document.getElementById('prompt2Mark').value;
        } else if (document.getElementById('prompt3Mark').checked) {
            promptButtonId = document.getElementById('prompt3Mark').value;
        }
        if (document.getElementById('word1Mark').checked) {
            wordButtonId = document.getElementById('word1Mark').value;
        } else if (document.getElementById('word2Mark').checked) {
            wordButtonId = document.getElementById('word2Mark').value;
        } else if (document.getElementById('word3Mark').checked) {
            wordButtonId = document.getElementById('word3Mark').value;
        }
        console.log(promptButtonId);
        console.log(wordButtonId);
        if(promptButtonId != null && wordButtonId != null) {
            socket.emit('submitPrompt', {lobbyName: sessionStorage.getItem('lobbyName'), 
                prompt: document.getElementById(promptButtonId).innerHTML, 
                word: document.getElementById(wordButtonId).innerHTML});
        }
        return false;
    });

    socket.on('redirect', function(destination) {
        console.log('works');
        window.location.href = destination;
        socket.emit('disconnect_request');
    });

    document.getElementById('playerName').innerHTML = sessionStorage.getItem('playerName')
});