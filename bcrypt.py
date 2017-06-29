from flask import Flask
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/generate-hash/<slug>')
def generate_hash(slug):
    pw_hash = bcrypt.generate_password_hash(slug)
    return {
      'hash': pw_hash
    }
    
@app.route('/check-hash/<slug>/<checksum>')
def check_hash(slug, checksum):
    pw_hash = bcrypt.generate_password_hash(slug)
    return {
      'is_same': bcrypt.check_password_hash(pw_hash, checksum)
    }

if __name__ == '__main__':
    app.run()
