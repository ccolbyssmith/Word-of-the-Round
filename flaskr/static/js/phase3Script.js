$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    socket.on('connect', function() {
        socket.emit('rejoin_lobby', sessionStorage.getItem('lobbyName'));
        socket.emit('loadPlayerScores', {lobbyName: sessionStorage.getItem('lobbyName')});
        socket.emit('loadChosenPrompt', sessionStorage.getItem('lobbyName'));
        socket.emit('loadInfo', {lobbyName: sessionStorage.getItem('lobbyName')});
        if (sessionStorage.getItem('isJudge') != 'true') {
            document.getElementById('answerMark1').disabled = true;
            document.getElementById('answerMark2').disabled = true;
            document.getElementById('answerMark3').disabled = true;
            document.getElementById('answerMark4').disabled = true;
            document.getElementById('answerMark5').disabled = true;
            document.getElementById('answerMark6').disabled = true;
            document.getElementById('chooseAnswer').style.display = 'none';
        }
        socket.emit('loadAnswers', sessionStorage.getItem('lobbyName'));
    });

    socket.on('displayChosenPrompt', function(info) {
        document.getElementById("Prompt").innerHTML = 'Prompt: ' + info['prompt'];
        document.getElementById("Word").innerHTML= 'Word: ' + info['word'];
    });

    socket.on('getInfo', function(info) {
        document.getElementById('win_data').innerHTML = 'Required Score to Win: ' + info['win_data']
    });

    socket.on('displayAnswers', function(answers) {
        console.log(answers);
        for (var i = 1; i <= answers.length; i++) {
            document.getElementById('answerNumber' + i).innerHTML = answers[i - 1];
        }
        for (var i = 6; i > answers.length; i--) {
            id = 'answerNumber' + i
            document.getElementById('answerNumber' + i).style.display = 'none';
            document.getElementById('answerMark' + i).style.display = 'none';
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
        console.log('works');
        window.location.href = destination;
        socket.emit('disconnect_request');
    });

    $('form#chooseAnswer').submit(function(event) {
        var answerButtonId;
        if (document.getElementById('answerMark1').checked) {
            answerButtonId = document.getElementById('answerMark1').value;
        } else if (document.getElementById('answerMark2').checked) {
            answerButtonId = document.getElementById('answerMark2').value;
        } else if (document.getElementById('answerMark3').checked) {
            answerButtonId = document.getElementById('answerMark3').value;
        } else if (document.getElementById('answerMark4').checked) {
            answerButtonId = document.getElementById('answerMark4').value;
        } else if (document.getElementById('answerMark5').checked) {
            answerButtonId = document.getElementById('answerMark5').value;
        } else if (document.getElementById('answerMark6').checked) {
            answerButtonId = document.getElementById('answerMark6').value;
        }
        console.log(answerButtonId);
        if(answerButtonId != null) {
            socket.emit('choseAnswer', {lobbyName: sessionStorage.getItem('lobbyName'), 
                answer: document.getElementById(answerButtonId).innerHTML});
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