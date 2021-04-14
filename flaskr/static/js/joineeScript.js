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