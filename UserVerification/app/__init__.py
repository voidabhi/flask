#importing flask and extensions
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.login import LoginManager

#initializing app from config based on production,development env
app = Flask(__name__)
app.config.from_object('config')

#initializing extensions
db = SQLAlchemy(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#importing custom modules
from app import views
from app import models
from app import forms