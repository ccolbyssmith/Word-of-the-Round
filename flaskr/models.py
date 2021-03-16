from .__init__ import db

class Lobby(db.Model):
	id = db.Column(db.Integer, primary_key = True, nullable = False)
	name = db.Column(db.String(8), unique = True, nullable = False)
	players = db.relationship("Player")
	
	def __repr__(self):
		return self.name

class Player(db.Model):
	id = db.Column(db.Integer, primary_key = True, nullable = False)
	name = db.Column(db.String, unique = False, nullable = False)
	lobby_id = db.Column(db.Integer, db.ForeignKey('lobby.id'), nullable = False)

	def __repr__(self):
		return self.name

def init_db():
	db.create_all()

if __name__ == '__main__':
    init_db()