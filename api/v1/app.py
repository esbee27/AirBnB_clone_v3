#!/usr/bin/python3
"""
This module initializes and configures the Flask application.
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
cors = CORS(app, send_wildcard=True)


@app.teardown_appcontext
def close(code):
    """
    Closes the storage on teardown of the Flask app context.

    Args:
        code: The status code.
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """
    Handles 404 errors by returning a JSON-formatted error message.

    Args:
        error: The error object.

    Returns:
        A JSON response with the error message and a 404 status code.
    """
    error_msg = {"error": "Not found"}
    return jsonify(error_msg), 404


if __name__ == "__main__":
    CORS(app, resources={'/*': {'origins': '0.0.0.0'}})
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', '6000')
    app.run(host=host, port=port, threaded=True)
