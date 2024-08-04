#!/usr/bin/python3
"""Flask application"""

from flask import Flask, render_template
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from flask import make_response, jsonify
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close_err(error):
    """Closes storage"""
    storage.close()

if __name__ == "__main__":
    """Main function"""

    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)

def error(message, status_code):
    """a handler for 404 errors that returns a JSON-formatted 404 status code response
    """
    return make_response(jsonify(error="Not found"), 404)
