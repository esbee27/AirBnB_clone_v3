#!/usr/bin/python3
"""Flask application"""

from flask import Flask, render_template
from models import storage
from app_views import api.v1.views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_err(error):
    """Closes storage"""
    storage.close()

if __name_ == "__main__":
    """Main function"""

    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
	host = '0.0.0.0.0'
    if not port:
	port = '5000'
    app.run(host=host, port=port, threaded=True)
