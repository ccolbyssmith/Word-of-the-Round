$(document).ready(function() {
    async fetchLobbyName() {
        try {
            const response = await fetch(`/getData`, {
                method: 'GET',
                credentials: 'same-origin'
            });
            const lobbyName = await response.json()['myLobbyName'];
            return lobbyName;
        } catch (error) {
            console.error(error);
        }
    }

    async fetchPlayerID() {
        try {
            const response = await fetch(`/getData`, {
                method: 'GET',
                credentials: 'same-origin'
            });
            const playerID = await response.json()['myPlayerID'];
            return playerID;
        } catch (error) {
            console.error(error);
        }
    }

    var myLobbyName = await fetchLobbyName();
    var myPlayerID = await fetchPlayerID();

    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    // Event handler for new connections.
    // The callback function is invoked when a connection with the
    // server is established.
    socket.on('connect', function() {
        socket.emit('my_event', {room: $(myLobbyName)});
    });

    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data
    // to the client. The data is then displayed in the "Received"
    // section of the page.
    socket.on('my_response', function(msg, cb) {
        $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
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
        socket.emit('leave', {room: $(myLobbyName)});
        return false;
    });
    $('form#send_room').submit(function(event) {
        socket.emit('my_room_event', {room: $(myLobbyName), data: $('#room_data').val()});
        return false;
    });
    $('form#disconnect').submit(function(event) {
        socket.emit('disconnect_request');
        return false;
    });
});