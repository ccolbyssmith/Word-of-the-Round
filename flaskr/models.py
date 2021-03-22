import json

class dataManipulator:
	fileLocation = 'flaskr/data/data.json'
	
	def addLobby(self, newLobbyName):
		data = self.loadData()
		lobbies = json.loads(data['lobbies'])
		lobbies.append(newLobbyName)
		data['lobbies'] = json.dumps(lobbies)
		self.writeData(data)

	def deleteLobby(self, emptyLobby):
		data = self.loadData()
		lobbies = json.loads(data['lobbies'])
		lobbies.remove(emptyLobby)
		data['lobbies'] = json.dumps(lobbies)
		self.writeData(data)

	def lobbyExists(self, soughtLobbyName):
		data = self.loadData()
		lobbyList = json.loads(data['lobbies'])
		for lobbyName in lobbyList:
			if lobbyName == soughtLobbyName:
				return True
		return False
		
	def findLobbyLocation(self, soughtLobbyName):
		data = self.loadData()
		lobbyList = json.loads(data['lobbies'])
		count = 0;
		for lobbyName in lobbyList:
			if lobbyName == soughtLobbyName:
				return count
			count += 1
		return -1

	def findPlayerLocation(self, soughtPlayerID):
		data = self.loadData()
		for lobby in data['lobbies']:
			count = 0
			for player in data[lobby]:
				if player['playerID'] == soughtPlayerID:
					return [lobby, count]
				count += 1

	def addPlayer(self, playerID, playerName, lobbyName):
		data = self.loadData()
		playerList = []
		if data.get(lobbyName) != None:
			playerList = json.loads(data[lobbyName])
		playerList.append({'playerID': playerID, 'playerName': playerName})
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

	def loadData(self):
		with open(self.fileLocation, 'r') as read_file:
			return json.load(read_file)

	def writeData(self, data):
		with open(self.fileLocation, 'w') as write_file:
			json.dump(data, write_file)

	def createNewData(self):
		data = {'lobbies': '[]'}
		self.writeData(data)