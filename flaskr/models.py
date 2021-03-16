import uuid

class Lobby:
	def __init__(self):
		self.playerList = []
		self.name = str(uuid.uuid4()).split('-')[0] 
	
	def __repr__(self):
		return self.name

	def addPlayer(self, player):
		self.playerList.append(player)

	def removePlayer(self, player):
		self.playerList.remove(player)

	def findPlayer(self, playerID):
		for player in self.playerList:
			if player.id == playerID:
				return player
		return None

class Player:
	def __init__(self, name):
		self.id = str(uuid.uuid4())
		self.name = name

	def __repr__(self):
		return self.name

class LobbyList:
	def __init__(self):
		self.lobbyList = []

	def addLobby(self, newLobby):
		self.lobbyList.append(newLobby)

	def deleteLobby(self, emptyLobby):
		self.lobbyList.remove(emptyLobby)

	def findLobby(self, lobbyName):
		for lobby in self.lobbyList:
			if lobby.name == lobbyName:
				return lobby
		return None

	def findPlayer(self, playerID):
		for lobby in self.lobbyList:
			if lobby.findPlayer(playerID)!= None:
				return lobby.findPlayer(playerID)
		return None