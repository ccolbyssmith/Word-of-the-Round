$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    $('form#hostLobby').submit(function(event) {
        socket.emit('hostLobby', {playerName: document.getElementById('name').value});
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
});