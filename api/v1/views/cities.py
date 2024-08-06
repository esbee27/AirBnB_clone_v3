#!/usr/bin/python3
"""
This module defines routes for handling City objects via a RESTful API.
"""

from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State or creates a new City.

    Methods:
        GET: Returns the list of all City objects in a State.
        POST: Creates a new City object.

    Returns:
        A JSON response with the list of City objects or the newly
        created City object.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    if request.method == 'POST':
        try:
            content = request.get_json(force=True)
        except ValueError:
            return jsonify({'error': 'Not a JSON'}), 400

        if 'name' not in content:
            return jsonify({'error': 'Missing name'}), 400

        new_city = City(**content)
        new_city.state_id = state_id
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_city(city_id):
    """
    Retrieves, deletes, or updates a City object by its ID.

    Methods:
        GET: Retrieves a City object by ID.
        DELETE: Deletes a City object by ID.
        PUT: Updates a City object by ID.

    Args:
        city_id (str): The ID of the City object.

    Returns:
        A JSON response with the City object or an appropriate status code.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        try:
            content = request.get_json(force=True)
        except ValueError:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, value in content.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)

        storage.save()
        return jsonify(city.to_dict()), 200
