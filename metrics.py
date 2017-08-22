from prometheus_client import Summary
from prometheus_client.exposition import generate_latest

from flask_restful import Resource
from flask import Response

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

class Metrics(Resource):
    """ Resource for exposing metrics to prometheus. """

    def get(self):
        """ get endpoint """

        latest = generate_latest()
        resp = Response(latest, headers={'Content-Type': 'text/plain'})

        return resp
