from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    error_msg = {"status": "OK"}
    return jsonify(error_msg)