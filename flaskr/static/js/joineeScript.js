$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

	$('form#joinLobby').submit(function(event) {
        socket.emit('joiningLobby', {playerName: document.getElementById('name').value, 
            lobbyName: document.getElementById('game id').value});
        return false;
    });

    socket.on('redirect', function(info) {
        sessionStorage.setItem('playerId', info['playerId']);
        sessionStorage.setItem('lobbyName', info['lobbyName']);
        sessionStorage.setItem('isHost', info['host']);
        sessionStorage.setItem('playerName', info['playerName']);
        window.location.href = info['destination'];
        socket.emit('disconnect_request');
    });

    socket.on('error', function() {
        document.getElementById('error').innerHTML = 'Error: Invalid Game ID'
    });
});