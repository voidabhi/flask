# adding imports
import os
import sqlite3
from flask import Flask ,request,session,g,redirect,url_for,render_template , abort,flash

# initializing app
app = Flask(__name__)

#configuration
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# basic endpoint
@app.route('/')
def hello_world():
    return 'Hello World!'

# initializing db 
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql',mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """
    Opens database connection in application context if it not already exist
    """
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    else :
        return g.sqlite_db


@app.teardown_appcontext
def close_db():
    """
    Closes the database connection afte the completion of request
    """
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

@app.route("/")
def show_entries():
    db = get_db()
    cur = db.execute('select title,text from entries order by id desc')
    entries = cur.fetch_all()
    return render_template('show_entries.html',entries=entries)

@app.route('/add',methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries(text,title) values (?,?)',[request.form['text'],request.form['title']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
