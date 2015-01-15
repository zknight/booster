from booster import app, db
from datetime import datetime

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    tease = db.Column(db.Text)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    expiry = db.Column(db.DateTime)

    @staticmethod
    def get_expired():
        return News.query.filter(News.expiry < datetime.now()).order_by(News.created_at).all()

    @staticmethod
    def get_current():
        return News.query.filter(News.expiry >= datetime.now()).order_by(News.created_at).all()

    @property
    def expiry_time(self):
        return self.expiry.time()
    
    @property
    def expiry_date(self):
        return self.expiry.date()

