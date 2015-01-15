from booster import app, db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
