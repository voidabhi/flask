__author__ = 'ABHIJEET'

from authomatic.providers import oauth2, oauth1

CONFIG = {

    'tw': { # Your internal provider name

        # Provider class
        'class_': oauth1.Twitter,

        # Twitter is an AuthorizationProvider so we need to set several other properties too:
        'consumer_key': 'QWYQgK4je6wRXi1jcFweW7WSo',
        'consumer_secret': '2k6KEKvtHjwEyVNAEyDfGqDjMDec7xdARCnptTZRa56PregJXo',
    },

    'fb': {

        'class_': oauth2.Facebook,

        # Facebook is an AuthorizationProvider too.
        'consumer_key': '134826863334136',
        'consumer_secret': '1e50633d5346bead543ad6d8d875cf9d',

        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_about_me', 'email', 'publish_stream'],
    }
}