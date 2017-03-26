###############################################
#### LOGGING CLASS SETTINGS (py25+, py30+) ####
###############################################
#### also will work with py23, py24 without 'encoding' arg
import logging
import logging.handlers
f = logging.Formatter(fmt='%(levelname)s:%(name)s: %(message)s '
    '(%(asctime)s; %(filename)s:%(lineno)d)',
    datefmt="%Y-%m-%d %H:%M:%S")
handlers = [
    logging.handlers.RotatingFileHandler('rotated.log', encoding='utf8',
        maxBytes=100000, backupCount=1),
    logging.StreamHandler()
]
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
for h in handlers:
    h.setFormatter(f)
    h.setLevel(logging.DEBUG)
    root_logger.addHandler(h)
##############################
#### END LOGGING SETTINGS ####
##############################


####################################################
#### LOGGING FILECONFIG SETTINGS (py26+, py30+) ####
####################################################

# logging.conf contents:
"""
[loggers]
keys=root
[handlers]
keys=consoleHandler,rotateFileHandler
[formatters]
keys=simpleFormatter
[logger_root]
level=DEBUG
handlers=consoleHandler,rotateFileHandler
[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)
[handler_rotateFileHandler]
class=handlers.RotatingFileHandler
level=DEBUG
formatter=simpleFormatter
args=('rotated.log', 'a', 100000, 1, 'utf8')
[formatter_simpleFormatter]
format=%(levelname)s:%(name)s: %(message)s (%(asctime)s; %(filename)s:%(lineno)d)
datefmt=%Y-%m-%d %H:%M:%S
"""

import logging
import logging.config
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
#########################################
#### END LOGGING FILECONFIG SETTINGS ####
#########################################


####################################################
#### LOGGING DICTCONFIG SETTINGS (py27+, py32+) ####
####################################################
import logging
import logging.config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                    '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'rotate_file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'rotated.log',
            'encoding': 'utf8',
            'maxBytes': 100000,
            'backupCount': 1,
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'rotate_file'],
            'level': 'DEBUG',
        },
    }
}
logging.config.dictConfig(LOGGING)
#########################################
#### END LOGGING DICTCONFIG SETTINGS ####
#########################################
