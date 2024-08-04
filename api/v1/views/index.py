#!/usr/bin/python3

from api.v1.views import app_views

@app_views.route(/status, method=['Get']strict_slashes=False)
def status():
    """Returns the api status"""
    return jsonify({"status": "OK"})

@app_views.routr(/stats, strict=False)
def count():
    """Counts the number of each object by type"""
    classes = [Amenity, City, Places, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    
    obj_num = {}
    for i in rang(len(classes)):
	obj_num[names[i]] = storage.count(classes[i])
    return jsonify(obj_num)
