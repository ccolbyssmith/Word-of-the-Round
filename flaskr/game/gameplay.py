import random
import json

class CardHandler:
	def __init__(self, cardType):
		if cardType == "prompts":
			self.load_fileLocation = 'flaskr/data/prompts.txt'
			self.write_fileLocation = 'flaskr/data/promptDecks.json'
			self.currentCardLocation = 'flaskr/data/currentPrompts.json'
			self.chosenCardLocation = 'flaskr/data/chosenPrompts.json'
		elif cardType == "words":
			self.load_fileLocation = 'flaskr/data/words.txt'
			self.write_fileLocation = 'flaskr/data/wordDecks.json'
			self.currentCardLocation = 'flaskr/data/currentWords.json'
			self.chosenCardLocation = 'flaskr/data/chosenWords.json'

	def createDeck(self):
		deck = []
		with open(self.load_fileLocation, 'r') as read_file:
			lines = read_file.readlines()
			for line in lines:
				deck.append({"text": line, "used": False})
		return deck
	
	def loadDeck(self, lobby):
		with open(self.write_fileLocation, 'r') as read_file:
			decks = json.load(read_file)
			deck = json.loads(decks[lobby])
			return deck

	def saveDeck(self, deck, lobby):
		decks = {}
		try:
			with open(self.write_fileLocation, 'r') as read_file:
				decks = json.loads(read_file)
		except:
			pass
		decks[lobby] = deck
		with open(self.write_fileLocation, 'w') as write_file:
			json.dump(decks, write_file)

	def saveCurrentCards(self, cards, lobby):
		currentCards = {}
		with open(self.currentCardLocation, 'r') as read_file:
			currentCards = json.load(read_file)
		cardDict = {'card1': cards[0], 'card2': cards[1], 'card3': cards[2]}
		currentCards[lobby] = cardDict
		with open(self.currentCardLocation, 'w') as write_file:
			json.dump(currentCards, write_file)

	def getCurrentCards(self, lobby):
		with open(self.currentCardLocation, 'r') as read_file:
			currentCards = json.load(read_file)
			print(currentCards[lobby])
			return currentCards[lobby]

	def saveChosenCard(self, card, lobby):
		chosenCards = {}
		with open(self.chosenCardLocation, 'r') as read_file:
			chosenCards = json.load(read_file)
		chosenCards[lobby] = card
		with open(self.chosenCardLocation, 'w') as write_file:
			json.dump(chosenCards, write_file)

	def getChosenCard(self, lobby):
		with open(self.chosenCardLocation, 'r') as read_file:
			chosenCards = json.load(read_file)
			return chosenCards[lobby]

	def useCard(self, deck, usedCard):
		for card in deck:
			if usedCard == card['text']:
				card['used'] = True
		return deck

	def return3Cards(self, lobby):
		deck = []
		try:
			deck = self.loadDeck(lobby)
		except:
			deck = self.createDeck()
		usableCards = []
		for card in deck:
			if card['used'] == False:
				usableCards.append(card['text'])
		chosenCards = []
		for i in range(0, 3):
			if len(usableCards) == 0:
				self.refreshDeck(deck)
				for card in self.deck:
					if card['used'] == False:
						usableCards.append(card['text'])
			chosenCards.append(usableCards[random.randint(0, len(usableCards) - 1)])
			usableCards.remove(chosenCards[i])
			deck = self.useCard(deck, chosenCards[i])
		self.saveDeck(deck, lobby)
		self.saveCurrentCards(chosenCards, lobby)
		return chosenCards

	def refreshDeck(self, deck):
		for card in deck:
			card['used'] = False
		return deck

	def returnCardCount(self, deck):
		count = 0
		for card in deck:
			if card['used'] == False:
				count += 1
		return count