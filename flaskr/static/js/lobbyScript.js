$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    // Event handler for new connections.
    // The callback function is invoked when a connection with the
    // server is established.
    socket.on('connect', function() {
        socket.emit('join_lobby', {playerId: sessionStorage.getItem('playerId')});
    });

    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data
    // to the client. The data is then displayed in the "Received"
    // section of the page.
    socket.on('server_response', function(msg) {
        socket.emit('loadPlayerList', {lobbyName: sessionStorage.getItem('lobbyName')});
        $('#log').append('<br>' + $('<div/>').text('Event: ' + msg.data).html());
    });

    socket.on('failedToStart', function() {
        document.getElementById('error').innerHTML = 'Not Enough Players To Start the Game'
    });

    socket.on('newHost', function(host) {
        if (host == sessionStorage.getItem('playerId')) {
            sessionStorage.setItem('isHost', true);
        }
        if (sessionStorage.getItem('isHost') == 'true') {
            document.getElementById('start').style.display = "block";
        }
    });

    socket.on('displayPlayerList', function(players) {
        var playerString = players[0];
        for (i = 1; i < players.length; i++) {
            playerString = playerString +  ", " + players[i];
        }
		document.getElementById('player_list').innerHTML = "Players: " + playerString;
    });

    socket.on('my_response', function(msg) {
        $('#log').append('<br>' + $('<div/>').text(msg.user + ': ' + msg.data).html());
    });

    socket.on('createJudge', function(judgeId) {
        if (sessionStorage.getItem('playerId') == judgeId) {
            sessionStorage.setItem('isJudge', true)
        } else {
            sessionStorage.setItem('isJudge', false)
        }
        socket.emit('gogogo', sessionStorage.getItem('lobbyName'));
    });

    //used for redircting user to new url
    socket.on('redirect', function(destination) {
        window.location.href = destination;
        socket.emit('disconnect_request');
    });

    // Handlers for the different forms in the page.
    // These accept data from the user and send it to the server in a
    // variety of ways
    $('form#leave').submit(function(event) {
        socket.emit('loadNewHost', {lobbyName: sessionStorage.getItem('lobbyName')});
        socket.emit('leave', {user: sessionStorage.getItem('playerId'),
            lobbyName: sessionStorage.getItem('lobbyName')});
        localStorage.clear();
        return false;
    });
    $('form#send_room').submit(function(event) {
        socket.emit('my_room_event', {data: $('#room_data').val(), lobby: sessionStorage.getItem('lobbyName'), 
            user: sessionStorage.getItem('playerId')});
        return false;
    });
    $('form#start').submit(function(event) {
        socket.emit('start_game', {time_limit:  document.getElementById('Time Limit').value,
            word_difficulty: document.getElementById('Word Difficulty').value, 
            word_limit: document.getElementById('Word Count Limit').value,
            win_data: document.getElementById('win_data').value, lobbyName: sessionStorage.getItem('lobbyName')});
        return false;
    });

    var slider = document.getElementById("win_data");
    var output = document.getElementById("win_output");
    output.innerHTML = slider.value; // Display the default slider value

    // Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
        output.innerHTML = this.value;
    }

    var gameCode = sessionStorage.getItem('lobbyName');
    document.getElementById('game_code').innerHTML = "Game Code: " + gameCode;
    if (sessionStorage.getItem('isHost') == "false") {
        document.getElementById('start').style.display = "none";
    }
});