import msgpack
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    """
    >>> import msgpack
    >>> import requests
    >>> msgpack.unpackb(requests.get('http://0.0.0.0:5000/').content)
    [1, 2, 3]
    """
    return msgpack.packb([1, 2, 3])


if __name__ == '__main__':
    app.run(debug=True)
