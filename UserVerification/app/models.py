
from app import app
from app import db
from datetime import datetime
from utils import hash_password
import scrypt

class User(db.Model):
    __tablename__ = "user1"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.LargeBinary())
    token = db.Column(db.BigInteger, nullable=True, default=None)
    email = db.Column(db.String(191), unique=True)
    new_email = db.Column(db.String(191), unique=True)
    is_verified = db.Column(db.Boolean)
    registered = db.Column(db.DateTime)

    def __init__(self, username, password, email, is_verified = False):
        self.username = username
        self.password = hash_password(password)
        self.email = email
        self.new_email = email
        self.is_verified = is_verified
        self.registered = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        return self.id

    def is_active(self):
        return self.is_verified

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def getVerificationHash(self):
        # combine a few properties, hash it
        # take first 16 chars for simplicity
        # make it email specific
        hash = scrypt.hash(str(self.username) + str(self.new_email), app.config['SECRET_KEY'])
        return hash.encode('hex')[:16]

    def getResetToken(self):
        # combine a few properties, hash it
        # take first 16 chars for simplicity
        hash = scrypt.hash(str(self.token), app.config['SECRET_KEY'])
        return hash.encode('hex')[:16]
