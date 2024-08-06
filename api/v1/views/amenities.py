#!/usr/bin/python3
"""
This module defines routes for handling Amenity objects via a RESTful API.
"""

from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects or creates a new Amenity.

    Methods:
        GET: Returns the list of all Amenity objects.
        POST: Creates a new Amenity object.

    Returns:
        A JSON response with the list of Amenity objects or the newly
        created Amenity object.
    """
    if request.method == 'GET':
        amenities = storage.all(Amenity)
        return jsonify([amenity.to_dict() for amenity in amenities.values()])

    if request.method == 'POST':
        try:
            content = request.get_json(force=True)
        except ValueError:
            return jsonify({'error': 'Not a JSON'}), 400

        if 'name' not in content:
            return jsonify({'error': 'Missing name'}), 400

        new_amenity = Amenity(**content)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves, deletes, or updates an Amenity object by its ID.

    Methods:
        GET: Retrieves an Amenity object by ID.
        DELETE: Deletes an Amenity object by ID.
        PUT: Updates an Amenity object by ID.

    Args:
        amenity_id (str): The ID of the Amenity object.

    Returns:
        A JSON response with the Amenity object or an appropriate status code.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        try:
            content = request.get_json(force=True)
        except ValueError:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, value in content.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)

        storage.save()
        return jsonify(amenity.to_dict()), 200
