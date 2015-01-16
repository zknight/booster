from booster import app, db

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    filename = db.Column(db.String(128))
