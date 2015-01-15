from booster import app, db

class EventType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(256))
    events = db.relationship('Event', backref='event_type', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('event_type.id'))
    name = db.Column(db.String(128))
    text = db.Column(db.Text)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    def __init__(self, name, text, start_time, end_time, type_id):
        self.type_id = type_id
        self.name = name
        self.text = text
        self.start_time = start_time
        self.end_time = end_time


