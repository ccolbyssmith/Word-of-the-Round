$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

	$('form#joinLobby').submit(function(event) {
        console.log('right Function')
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

    socket.on('refresh', function() {
        location.reload();
    });
});

fetch('/Word_of_the_Round/getJoinError')
	.then(response => response.json())
	.then(errorValue => {
		var joinError = errorValue['joinError']
		var errorMsg = ''
		if (joinError == true) {
			errorMsg = 'This Lobby Does Not Exist'
		} else {
			errorMsg = ''
		}
		document.getElementById('error').innerHTML = errorMsg
	});