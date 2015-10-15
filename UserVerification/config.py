__author__ = 'ABHIJEET'

"""
    Flask Configuration
"""
HOST = '127.0.0.1'
PORT = 5000
DEBUG = True
SECRET_KEY = 'SuperSecretString'

"""
    Logging Configuration
"""
LOG_FILE = 'app.log'
LOG_LEVEL = 'DEBUG'
LONG_NAME='This is a very long name'

"""
    Database Configuration
"""
DB_USER = 'root'
DB_PASS = ''
DB_NAME = 'tz'
DB_HOST = '127.0.0.1'
DB_CREATED = False
SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASS + '@' + DB_HOST + ':3306/' + DB_NAME

"""
    Mail Configuration
"""
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'dmonstermaker'
MAIL_PASSWORD = 'antihacking'

"""
    Site Configuration
"""
DOMAIN_NAME = 'example.com'
SITE_NAME = 'UserVerification'
SITE_ICON = 'icon-code'

CONTACT_MAIL = 'info@' + DOMAIN_NAME
COPYRIGHT_NOTICE = '&copy; 2014 ' + DOMAIN_NAME.lower() + ', all rights reserved.'
COPY_MAIL = 'newsgags@gmail.com'

"""
    Form Configuration
"""
CSRF_ENABLED = True
CSRF_SESSION_KEY = "something-impossible-to-guess"

"""
    Recaptcha constants
"""
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
RECAPTCHA_OPTIONS = {'theme': 'white'}
