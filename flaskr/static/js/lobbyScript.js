$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    // Event handler for new connections.
    // The callback function is invoked when a connection with the
    // server is established.
    socket.on('connect', function() {
        console.log(sessionStorage.getItem('playerId'));
        socket.emit('join_lobby', {playerId: sessionStorage.getItem('playerId')});
    });

    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data
    // to the client. The data is then displayed in the "Received"
    // section of the page.
    socket.on('server_response', function(msg, cb) {
        socket.emit('loadPlayerList', {lobbyName: sessionStorage.getItem('lobbyName')});
        $('#log').append('<br>' + $('<div/>').text('Event: ' + msg.data).html());
        if (cb)
            cb();
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

    socket.on('my_response', function(msg, cb) {
        console.log(msg.user);
        $('#log').append('<br>' + $('<div/>').text(msg.user + ': ' + msg.data).html());
        if (cb)
            cb();
    });


    //used for redircting user to new url
    socket.on('redirect', function(destination, cb) {
        console.log('works')
        window.location.href = destination;
        socket.emit('disconnect_request');
        if (cb)
            cb();
    });

    // Interval function that tests message latency by sending a "ping"
    // message. The server then responds with a "pong" message and the
    // round trip time is measured.
    var ping_pong_times = [];
    var start_time;
    window.setInterval(function() {
        start_time = (new Date).getTime();
        socket.emit('my_ping');
    }, 1000);

    // Handler for the "pong" message. When the pong is received, the
    // time from the ping is stored, and the average of the last 30
    // samples is average and displayed.
    socket.on('my_pong', function() {
        var latency = (new Date).getTime() - start_time;
        ping_pong_times.push(latency);
        ping_pong_times = ping_pong_times.slice(-30); // keep last 30 samples
        var sum = 0;
        for (var i = 0; i < ping_pong_times.length; i++)
            sum += ping_pong_times[i];
        $('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
    });

    // Handlers for the different forms in the page.
    // These accept data from the user and send it to the server in a
    // variety of ways
    $('form#leave').submit(function(event) {
        socket.emit('leave', {user: sessionStorage.getItem('playerId'),
            lobbyName: sessionStorage.getItem('lobbyName')});
        return false;
    });
    $('form#send_room').submit(function(event) {
        socket.emit('my_room_event', {data: $('#room_data').val(), lobby: sessionStorage.getItem('lobbyName'), 
            user: sessionStorage.getItem('playerId')});
        return false;
    });
    $('form#start').submit(function(event) {
        console.log(document.getElementById('Time Limit').value);
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
    console.log(sessionStorage.getItem('isHost'));
    if (sessionStorage.getItem('isHost') == "false") {
        document.getElementById('start').style.display = "none";
    }
});