from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# initializing app and db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# User model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    # model constructor
    def __init__(self, username, email):
        self.username = username
        self.email = email

    # representation of object when printed
    def __repr__(self):
        return '<User %r>' % self.username

# index endpoint
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
