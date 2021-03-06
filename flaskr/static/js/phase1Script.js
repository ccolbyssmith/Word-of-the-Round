$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    socket.on('connect', function() {
        socket.emit('rejoin_lobby', sessionStorage.getItem('lobbyName'));
        socket.emit('loadInfo', {lobbyName: sessionStorage.getItem('lobbyName')});
        socket.emit('loadPlayerScores', {lobbyName: sessionStorage.getItem('lobbyName')});
    });

    socket.on('drewPrompts', function() {
        sessionStorage.setItem('gotPrompts', 'true');
        socket.emit('loadPrompts', {lobbyName: sessionStorage.getItem('lobbyName')});
    });

    socket.on('displayPrompts', function(prompts) {
        sessionStorage.setItem('gotPrompts', 'true');
        document.getElementById('Prompt1').innerHTML = prompts['prompt1'];
        document.getElementById('Prompt2').innerHTML = prompts['prompt2'];
        document.getElementById('Prompt3').innerHTML = prompts['prompt3'];
        document.getElementById('Word1').innerHTML = prompts['word1'];
        document.getElementById('Word2').innerHTML = prompts['word2'];
        document.getElementById('Word3').innerHTML = prompts['word3'];
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

    socket.on('newHost', function(host) {
        if (host == sessionStorage.getItem('playerId')) {
            sessionStorage.setItem('isHost', true);
        }
    });

    socket.on('getInfo', function(info) {
        if (sessionStorage.getItem('playerId') == info['judgeId'] && sessionStorage.getItem('gotPrompts') != 'true') {
            sessionStorage.setItem('gotPrompts', true);
            sessionStorage.setItem('isJudge', true);
            socket.emit('drawPrompts', {lobbyName: sessionStorage.getItem('lobbyName')});
        }
        socket.emit('loadPrompts', {lobbyName: sessionStorage.getItem('lobbyName')});
        if (sessionStorage.getItem('playerId') != info['judgeId']) {
            sessionStorage.setItem('isJudge', false);
        }
        if (sessionStorage.getItem('playerId') != info['judgeId']) {
            document.getElementById('prompt1Mark').disabled = true;
            document.getElementById('prompt2Mark').disabled = true;
            document.getElementById('prompt3Mark').disabled = true;
            document.getElementById('word1Mark').disabled = true;
            document.getElementById('word2Mark').disabled = true;
            document.getElementById('word3Mark').disabled = true;
            document.getElementById('submitPrompt').style.display = 'none';
        }
        document.getElementById('win_data').innerHTML = 'Required Score to Win: ' + info['win_data']
    });

    $('form#leave').submit(function(event) {
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
        if(promptButtonId != null && wordButtonId != null) {
            socket.emit('submitPrompt', {lobbyName: sessionStorage.getItem('lobbyName'), 
                prompt: document.getElementById(promptButtonId).innerHTML, 
                word: document.getElementById(wordButtonId).innerHTML});
        }
        return false;
    });

    socket.on('redirect', function(destination) {
        sessionStorage.setItem('gotPrompts', false);
        window.location.href = destination;
        socket.emit('disconnect_request');
    });

    document.getElementById('playerName').innerHTML = sessionStorage.getItem('playerName')
});