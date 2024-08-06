#!/usr/bin/python3
"""
This module defines routes for the status and stats endpoints.
"""

from flask import jsonify
from models import storage
from api.v1.views import app_views

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns the status of the API.

    Returns:
        JSON response with a status message.
    """
    msg = {"status": "OK"}
    return jsonify(msg)


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Retrieves the count of each object by type.

    Returns:
        JSON response with the count of each object.
    """
    dic = {}
    for cls in classes.keys():
        dic[cls] = storage.count(classes[cls])
    return jsonify(dic)


if __name__ == "__main__":
    pass
