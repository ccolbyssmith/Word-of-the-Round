class CardHandler:
	def __init__(self, new, cardType, lobby):
		if cardType == "prompts":
			self.load_fileLocation = 'flaskr/data/prompts.txt'
		elif cardType == "words":
			self.load_fileLocation = 'flaskr/data/words.txt'
		self.write_fileLocation = 'flaskr/data/decks.json'
		if new == True:
			self.createDeck()
		else:
			self.loadDeck()
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
			json.dumps(self.decks, write_file)

	def useCard(self, usedCard):
		for card in self.deck:
			if usedCard = card['prompt']:
				card['used'] = True

	def returnPrompts(self):
		usablePrompts = []
		for card in self.deck:
			if card['used'] = False:
				usablePrmpts.append(card['prompt'])

	def refreshDeck(self):
		for card in self.deck:
			card['used'] = False

	def returnCardCount(self):
		count = 0
		for card in self.deck:
			if card['used'] = False:
				count += 1
		return count