from booster import app, db
from sqlalchemy.ext.hybrid import hybrid_property
#from booster.models import Picture

product_pics = db.Table('product_pics',
        db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
        db.Column('picture_id', db.Integer, db.ForeignKey('picture.id'))
        )

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    instock = db.Column(db.Boolean)
    price = db.Column(db.Integer)
    pictures = db.relationship('Picture', secondary=product_pics,
            backref='products', lazy='dynamic')

    @property
    def dollars(self):
        return float(self.price / 100.0)

    @dollars.setter
    def dollars(self, amt):
        self.price = int(amt * 100)

