#!/usr/bin/python3

from api.v1.views import app_views

@app_views.route(/status, method=['Get']strict_slashes=False)
def status():
	"""Returns the api status"""
	return jsonify({"status": "OK"})
