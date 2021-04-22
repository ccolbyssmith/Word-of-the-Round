class PromptDeck:
	fileLocation = 'flaskr/data/prompts.json'

	def __init__(self):
		self.createDeck()


	def createDeck(self):
		self.deck = []
		with open(self.fileLocation, 'r') as read_file:
			lines = read_file.readlines()
			for line in lines:
				self.deck.append(line)
			

class WordDeck:
	fileLocation = 'flaskr/data/words.json'

	def __init__(self):
		self.createDeck()

	def createDeck(self):
		self.deck = []
		with open(self.fileLocation, 'r') as read_file:
			lines = read_file.readlines()
			for line in lines:
				self.deck.append(line)