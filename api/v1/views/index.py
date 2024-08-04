#!/usr/bin/python3

from api.v1.views import app_views
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the api status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict=False)
def count():
    """Counts the number of each object by type"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    
    obj_num = {}
    for i in range(len(classes)):
        obj_num[names[i]] = storage.count(classes[i])
        return jsonify(obj_num)
