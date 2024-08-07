#!/usr/bin/python3
"""
This module defines routes for handling User objects via a RESTful API.
"""

from flask import jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def handle_users():
    """
    Retrieves all User objects or creates a new User object.

    - GET: Returns a list of all User objects.
    - POST: Creates a new User object with the provided data.

    Returns:
        - GET: JSON list of User objects.
        - POST: JSON representation of the newly created User object.
    """
    if request.method == 'GET':
        objects = storage.all(User)
        obj_list = [value.to_dict() for value in objects.values()]
        return jsonify(obj_list)
    elif request.method == 'POST':
        try:
            content = request.get_json()
        except ValueError:
            return jsonify({'error': 'Not a JSON'}), 400
        if not isinstance(content, dict):
            return jsonify({'error': 'Not a JSON'}), 400
        if 'email' not in content:
            return jsonify({'error': 'Missing email'}), 400
        if 'password' not in content:
            return jsonify({'error': 'Missing password'}), 400

        new_user = User(**content)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_user(user_id):
    """
    Retrieves, deletes, or updates a User object by its ID.

    - GET: Retrieves a User object by its ID.
    - DELETE: Deletes a User object by its ID.
    - PUT: Updates a User object with the provided data.

    Args:
        user_id (str): The ID of the User object.

    Returns:
        - GET: JSON representation of the User object.
        - DELETE: Empty JSON object with status code 200.
        - PUT: JSON representation of the updated User object.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            content = request.get_json()
        except ValueError:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, value in content.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
