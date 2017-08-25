import os
import sys

from flask import Flask

PROJECT_DIR, PROJECT_MODULE_NAME = os.path.split(
    os.path.dirname(os.path.realpath(__file__))
)

FLASK_JSONRPC_PROJECT_DIR = os.path.join(PROJECT_DIR, os.pardir)
if os.path.exists(FLASK_JSONRPC_PROJECT_DIR) \
        and not FLASK_JSONRPC_PROJECT_DIR in sys.path:
    sys.path.append(FLASK_JSONRPC_PROJECT_DIR)

from flask_jsonrpc import JSONRPC
from flask_jsonrpc.site import JSONRPCSite

app = Flask(__name__)
jsonrpc_v1 = JSONRPC(app, '/api/v1', site=JSONRPCSite(), enable_web_browsable_api=True)
jsonrpc_v2 = JSONRPC(app, '/api/v2', site=JSONRPCSite(), enable_web_browsable_api=True)

@jsonrpc_v1.method('App.index')
def index_v1():
    return u'Welcome to Flask JSON-RPC Version API 1'

@jsonrpc_v2.method('App.index')
def index_v2():
    return u'Welcome to Flask JSON-RPC Version API 2'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
