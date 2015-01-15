from booster import app, db
import bcrypt

class User(db.Model):
    ''' The only user is an administrator, so there aren't roles 
    '''
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(256), unique=True)
    smash = db.Column(db.String(64))
    is_super = db.Column(db.Boolean)

    def __init__(self, login, password, email, is_super=False):
        self.login = login
        self.email = email
        self.smash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
        self.is_super = is_super

    def authorize(self, password):
        if self.smash == bcrypt.hashpw(password.encode('utf-8'), self.smash.encode('utf-8')):
            return True
        return False


