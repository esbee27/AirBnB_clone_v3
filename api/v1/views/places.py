#!/usr/bin/python3
"""
This module defines routes for handling Place objects via a RESTful API.
"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """
    Retrieves the list of all Place objects in a given city.

    Args:
        city_id (str): The ID of the City object.

    Returns:
        A JSON response with the list of Place objects in the city.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object by its ID.

    Args:
        place_id (str): The ID of the Place object.

    Returns:
        A JSON response with the Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object by its ID.

    Args:
        place_id (str): The ID of the Place object.

    Returns:
        A JSON response indicating the deletion.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a new Place object in a given city.

    Args:
        city_id (str): The ID of the City object.

    Returns:
        A JSON response with the newly created Place object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    content = request.get_json()
    if not isinstance(content, dict):
        return jsonify({'error': 'Not a JSON'}), 400

    if 'user_id' not in content:
        return jsonify({'error': 'Missing user_id'}), 400

    user = storage.get(User, content['user_id'])
    if user is None:
        abort(404)

    if 'name' not in content:
        return jsonify({'error': 'Missing name'}), 400

    new_place = Place(**content)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def search_places():
    """
    Retrieves all Place objects based on the criteria in the request body.

    Returns:
        A JSON response with the list of Place objects that match the criteria.
    """
    body = request.get_json()
    if not isinstance(body, dict):
        return jsonify({'error': 'Not a JSON'}), 400

    id_states = body.get("states", [])
    id_cities = body.get("cities", [])
    id_amenities = body.get("amenities", [])

    places = []
    if not id_states and not id_cities:
        places = storage.all(Place).values()
    else:
        states = [storage.get(State, _id) for _id in id_states
                  if storage.get(State, _id)]
        cities = [city for state in states for city in state.cities]
        cities += [storage.get(City, _id) for _id in id_cities
                   if storage.get(City, _id)]
        cities = list(set(cities))
        places = [place for city in cities for place in city.places]

    amenities = [storage.get(Amenity, _id) for _id in id_amenities
                 if storage.get(Amenity, _id)]

    result = []
    for place in places:
        if all(amenity in place.amenities for amenity in amenities):
            result.append(place.to_dict())

    return jsonify(result)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object by its ID.

    Args:
        place_id (str): The ID of the Place object.

    Returns:
        A JSON response with the updated Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    content = request.get_json()
    if not isinstance(content, dict):
        return jsonify({'error': 'Not a JSON'}), 400

    for key, value in content.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
