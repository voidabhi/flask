import json
import hashlib
import flask
import flask.ext.sqlalchemy
import flask.ext.restless
from flask.ext.restless import ProcessingException

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = flask.ext.sqlalchemy.SQLAlchemy(app)

# using memcached:
from werkzeug.contrib.cache import MemcachedCache
cache = MemcachedCache(['127.0.0.1:11211'])

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)

db.create_all()
from flask import request

def get_cache_key():
    return hashlib.md5(request.path + request.query_string).hexdigest()

def cache_preprocessor(**kwargs):
    key = get_cache_key()
    if cache.get(key):
        print 'returning cached result'
        raise ProcessingException(description=cache.get(key), code=200)

def cache_postprocessor(result, **kwargs):
    cache.set(get_cache_key(), json.dumps(result))
    print 'result cached.'


manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Person,
                   methods=['GET'],
                   preprocessors={'GET_MANY': [cache_preprocessor]},
                   postprocessors={'GET_MANY': [cache_postprocessor]})

app.run()
