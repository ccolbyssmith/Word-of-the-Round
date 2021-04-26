$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    // Event handler for new connections.
    // The callback function is invoked when a connection with the
    // server is established.
    socket.on('connect', function() {
        socket.emit('join_lobby', {});
    });

    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data
    // to the client. The data is then displayed in the "Received"
    // section of the page.
    socket.on('server_response', function(msg, cb) {
        fetch('/Word_of_the_Round/getPlayers')
	        .then(response => response.json())
	        .then(players => {
                console.log(players);
                var playerString = players[0];
                for (i = 1; i < players.length; i++) {
                    playerString = playerString +  ", " + players[i];
                }
		        document.getElementById('player_list').innerHTML = "Players: " + playerString;
            });
        fetch('/Word_of_the_Round/getId')
	        .then(response => response.json())
	        .then(id => {
                console.log(id['host']);
                if (id['host'] == true) {
                    document.getElementById('start').style.display = "block";
                }
            });
        $('#log').append('<br>' + $('<div/>').text('Event: ' + msg.data).html());
        if (cb)
            cb();
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
        socket.emit('leave', {});
        return false;
    });
    $('form#send_room').submit(function(event) {
        socket.emit('my_room_event', {data: $('#room_data').val()});
        return false;
    });
    $('form#start').submit(function(event) {
        socket.emit('start_game', {time_limit: $('#Time Limit').val(),
        word_difficulty: $('Word Difficulty').val(), 
        word_limit: $('Word Count Limit').val(),
        win_data: $('win_data').val()});
        return false;
    });

    var slider = document.getElementById("win_data");
    var output = document.getElementById("win_output");
    console.log(slider.value);
    output.innerHTML = slider.value; // Display the default slider value

    // Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
      output.innerHTML = this.value;
      console.log(output.innerHTML);
}
});

fetch('/Word_of_the_Round/getId')
	.then(response => response.json())
	.then(id => {
		var gameCode = id['myLobbyName'];
		document.getElementById('game_code').innerHTML = "Game Code: " + gameCode;
        console.log(id['host'])
        if (id['host'] == false) {
            document.getElementById('start').style.display = "none";
        }
    });