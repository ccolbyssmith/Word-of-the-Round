import json

class DataManipulator:
	fileLocation = 'flaskr/data/data.json'
	
	def addLobby(self, newLobbyName):
		data = self.loadData()
		lobbies = json.loads(data['lobbies'])
		lobbies.append(newLobbyName)
		data['lobbies'] = json.dumps(lobbies)
		data[newLobbyName] = {}
		self.writeData(data)

	def deleteLobby(self, emptyLobby):
		data = self.loadData()
		lobbies = json.loads(data['lobbies'])
		lobbies.remove(emptyLobby)
		data['lobbies'] = json.dumps(lobbies)
		data.pop(emptyLobby)
		self.writeData(data)

	def lobbyExists(self, soughtLobbyName):
		data = self.loadData()
		lobbyList = json.loads(data['lobbies'])
		for lobby in lobbyList:
			if lobby == lobbyName:
				return True
		return False

	def gameStarted(self, lobbyName, settings):
		lobby = self.returnLobby(lobbyName)
		return lobby['started']

	def startGame(self, lobbyName, settings):
		data = self.loadData()
		data[lobbyName]['started'] = True
		data[lobbyName]['settings'] = {'time_limit': settings['time_limit'],
			'word_difficulty': settings['word_difficulty'], 'word_limit': settings['word_limit'],
			'win_data': settings['win_data']}
		self.writeData(data)

	def findPlayerLocation(self, soughtPlayerID):
		data = self.loadData()
		for lobby in json.loads(data['lobbies']):
			count = 0
			for player in json.loads(data[lobby]['players']):
				if player['playerID'] == soughtPlayerID:
					return [lobby, count]
				count += 1

	def findLobbyLocation(self, soughtLobbyName):
		data = self.loadData()
		lobbyList = json.loads(data['lobbies'])
		count = 0;
		for lobby in lobbyList:
			if lobby['lobbyName'] == soughtLobbyName:
				return count
			count += 1
		return -1

	def lobbyIsNew(self, lobbyName):
		return self.loadData()[lobbyName]['new']

	def makeLobbyOld(self, lobbyName):
		data = self.loadData()
		data[lobbyName]['new'] = False
		self.writeData(data)

	def returnPlayerName(self, soughtPlayerID):
		data = self.loadData()
		playerLocation = self.findPlayerLocation(soughtPlayerID)
		lobbyName = playerLocation[0]
		playerPosition = playerLocation[1]
		playerList = json.loads(data[lobbyName]['players'])
		return playerList[playerPosition]['playerName']

	def isHost(self, playerID):
		data = self.loadData()
		playerLocation = self.findPlayerLocation(playerID)
		lobbyName = playerLocation[0]
		playerPosition = playerLocation[1]
		playerList = json.loads(data[lobbyName]['players'])
		return playerList[playerPosition]['host']

	def addPlayer(self, playerID, playerName, lobbyName):
		data = self.loadData()
		playerList = []
		host = True
		if data[lobbyName].get('players') != None:
			playerList = json.loads(data[lobbyName])
			host = False
		playerList.append({'playerID': playerID, 'playerName': playerName, 'host': host})
		data[lobbyName]['players'] = json.dumps(playerList)
		self.writeData(data)

	def deletePlayer(self, playerID):
		data = self.loadData()
		playerLocation = self.findPlayerLocation(playerID)
		lobbyName = playerLocation[0]
		playerPosition = playerLocation[1]
		playerList = json.loads(data[lobbyName]['players'])
		if playerList[playerPosition]['host'] == True:
			if len(playerList) > 1:
				playerList[playerPosition + 1]['host'] = True
		playerList.pop(playerPosition)
		data[lobbyName] = json.dumps(playerList)
		self.writeData(data)

	def returnPlayerCount(self, lobbyName):
		data = self.loadData()
		count = 0
		for player in json.loads(data[lobbyName]['players']):
			count += 1
		return count

	def returnSettings(self, lobbyName):
		return self.loadData()[lobbyName]['settings']

	def loadData(self):
		with open(self.fileLocation, 'r') as read_file:
			return json.load(read_file)

	def loadPlayerList(self, lobbyName):
		data = self.loadData()
		return json.loads(data[lobbyName]['players'])

	def writeData(self, data):
		with open(self.fileLocation, 'w') as write_file:
			json.dump(data, write_file)

	def createNewData(self):
		data = {'lobbies': '[]'}
		self.writeData(data)