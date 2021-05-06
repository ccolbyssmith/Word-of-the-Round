import random

class CardHandler:
	def __init__(self, cardType):
		if cardType == "prompts":
			self.load_fileLocation = 'flaskr/data/prompts.txt'
		elif cardType == "words":
			self.load_fileLocation = 'flaskr/data/words.txt'
		self.write_fileLocation = 'flaskr/data/decks.json'
		self.createDeck()

	def addLobby(self, lobby):
		self.lobby = lobby

	def createDeck(self):
		self.deck = []
		with open(self.load_fileLocation, 'r') as read_file:
			lines = read_file.readlines()
			for line in lines:
				self.deck.append({"prompt": line, "used": False})
	
	def loadDeck(self):
		with open(self.write_fileLocation, 'r') as read_file:
			decks = json.load(read_file)
			self.deck = json.loads(decks[self.lobby])

	def saveDeck(self):
		decks = {}
		with open(self.write_fileLocation, 'r') as read_file:
			decks = json.loads(read_file)
		decks[self.lobby] = self.deck
		with open(self.write_fileLocation, 'w') as write_file:
			json.dumps(decks, write_file)

	def useCard(self, usedCard):
		for card in self.deck:
			if usedCard == card['prompt']:
				card['used'] = True

	def returnPrompts(self):
		usablePrompts = []
		for card in self.deck:
			if card['used'] == False:
				usablePrompts.append(card['prompt'])
		chosenPrompts = []
		for i in range(0, 3):
			chosenPrompts.append(usablePrompts[random.randint(0, len(usablePrompts))])
			usablePrompts.remove(chosenPrompts[i])
			self.useCard(chosenPrompts[i])
		self.saveDeck()
		return chosenPrompts

	def refreshDeck(self):
		for card in self.deck:
			card['used'] = False

	def returnCardCount(self):
		count = 0
		for card in self.deck:
			if card['used'] == False:
				count += 1
		return count