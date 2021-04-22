import json

class dataManipulator:
	fileLocation = 'flaskr/data/data.json'
	
	def addLobby(self, newLobbyName):
		data = self.loadData()
		lobbies = json.loads(data['lobbies'])
		lobbies.append({'lobbyName': newLobbyName, 'started': False})
		data['lobbies'] = json.dumps(lobbies)
		self.writeData(data)

	def deleteLobby(self, emptyLobby):
		data = self.loadData()
		lobbies = json.loads(data['lobbies'])
		for lobby in lobbies:
			if lobby['lobbyName'] == emptyLobby:		
				lobbies.remove(lobby)
		data['lobbies'] = json.dumps(lobbies)
		data.pop(emptyLobby)
		self.writeData(data)

	def lobbyExists(self, soughtLobbyName):
		if self.returnLobby(soughtLobbyName) == None:
			return False
		else:
			return True		

	def gameStarted(self, lobbyName):
		lobby = self.returnLobby(lobbyName)
		return lobby['started']

	def startGame(self, lobbyName):
		data = self.loadData()
		lobbies = json.loads(data['lobbies'])
		lobbyLocation = self.findLobbyLocation(lobbyName)
		lobbies[lobbyLocation]['started'] = True
		data['lobbies'] = json.dumps(lobbies)
		self.writeData(data)

	def findPlayerLocation(self, soughtPlayerID):
		data = self.loadData()
		for lobby in json.loads(data['lobbies']):
			count = 0
			for player in json.loads(data[lobby['lobbyName']]):
				if player['playerID'] == soughtPlayerID:
					return [lobby['lobbyName'], count]
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

	def returnPlayerName(self, soughtPlayerID):
		data = self.loadData()
		playerLocation = self.findPlayerLocation(soughtPlayerID)
		lobbyName = playerLocation[0]
		playerPosition = playerLocation[1]
		playerList = json.loads(data[lobbyName])
		return playerList[playerPosition]['playerName']

	def isHost(self, playerID):
		data = self.loadData()
		playerLocation = self.findPlayerLocation(playerID)
		lobbyName = playerLocation[0]
		playerPosition = playerLocation[1]
		playerList = json.loads(data[lobbyName])
		return playerList[playerPosition]['host']

	def addPlayer(self, playerID, playerName, lobbyName):
		data = self.loadData()
		playerList = []
		host = True
		if data.get(lobbyName) != None:
			playerList = json.loads(data[lobbyName])
			host = False
		playerList.append({'playerID': playerID, 'playerName': playerName, 'host': host})
		data[lobbyName] = json.dumps(playerList)
		self.writeData(data)

	def deletePlayer(self, playerID):
		data = self.loadData()
		playerLocation = self.findPlayerLocation(playerID)
		lobbyName = playerLocation[0]
		playerPosition = playerLocation[1]
		playerList = json.loads(data[lobbyName])
		playerList.pop(playerPosition)
		data[lobbyName] = json.dumps(playerList)
		self.writeData(data)

	def returnPlayerCount(self, lobbyName):
		data = self.loadData()
		count = 0
		for player in json.loads(data[lobbyName]):
			count += 1
		return count

	def returnLobby(self, lobbyName):
		data = self.loadData()
		lobbyList = json.loads(data['lobbies'])
		for lobby in lobbyList:
			if lobby['lobbyName'] == lobbyName:
				return lobby
		print("lobby doesn't exist'")
		return None

	def loadData(self):
		with open(self.fileLocation, 'r') as read_file:
			return json.load(read_file)

	def loadPlayerList(self, lobbyName):
		data = self.loadData()
		return json.loads(data[lobbyName])

	def writeData(self, data):
		with open(self.fileLocation, 'w') as write_file:
			json.dump(data, write_file)

	def createNewData(self):
		data = {'lobbies': '[]'}
		self.writeData(data)