#!/usr/bin/python3

from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import jsonify, Blueprint
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def close(code):
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    error_msg = {"error": "Not found"}
    return jsonify(error_msg), 404

if __name__ == "__main__":
    CORS(app, resources={'/*': {'origins': '0.0.0.0'}})
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', '6000')
    app.run(host = host, port = port, threaded=True)
