__author__ = 'ABHIJEET'

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField,BooleanField
from wtforms.validators import Required, EqualTo, Email,ValidationError,Length
from models import User

"""
    Custom Validators
"""

# User Exists
def username_exists(form,field):
    user = User.query.filter_by(username = field.data).first()
    if user:
        raise ValidationError('User with this username already exist!')

# User Not Exists
def username_not_exists(form,field):
    user = User.query.filter_by(username = field.data).first()
    if not user:
        raise ValidationError('User with this username not exist!')

# Email Exists
def email_exists(form,field):
    user = User.query.filter_by(email = field.data).first()
    if user:
        raise ValidationError('User with this email already exists!')

# Email not Exists
def email_not_exists(form,field):
    user = User.query.filter_by(email = field.data).first()
    if not user:
        raise ValidationError('User with this email doesn\'t exists!')


class LoginForm(Form):
      username = TextField('username', [Required()])
      password = PasswordField('Password', [Required()])
      remember_me = BooleanField('I accept the TOS', [Required()])

"""
class RegisterForm(Form):
      username = TextField('Username',[Required(),username_exists])
      name = TextField('Name', [Required()])
      email = TextField('Email address', [Required(), Email(),email_exists])
      password = PasswordField('Password', [Required()])
      confirm = PasswordField('Repeat Password', [
          Required(),
          EqualTo('password', message='Passwords must match')
          ])
      accept_tos = BooleanField('I accept the TOS', [Required()])
      recaptcha = RecaptchaField()
"""

class RegisterForm(Form):
      username = TextField('Name', [Required()])
      email = TextField('Email address', [Required(), Email(),email_exists])
      password = PasswordField('Password', [Required()])
      confirm = PasswordField('Repeat Password', [
          Required(),
          EqualTo('password', message='Passwords must match')
          ])

class RecoveryForm(Form):
      username = TextField('username',[Required(),Email(),username_not_exists])

class NewPasswordForm(Form):
    password = PasswordField("Password", validators=[Length(min=8, message = "Please enter a password of at least 8 characters.")])
    password2 = PasswordField("Password, again", validators=[EqualTo("password", "Passwords do not match.")])

