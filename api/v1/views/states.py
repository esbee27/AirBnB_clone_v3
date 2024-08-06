#!/usr/bin/python3
"""
This module defines routes for handling State objects via a RESTful API.
"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_state():
    """
    Retrieves the list of all State objects or creates a new State.

    Methods:
        GET: Returns the list of all State objects.
        POST: Creates a new State object.

    Returns:
        A JSON response with the list of State objects
        or the newly created State object.
    """
    if request.method == 'GET':
        objects = storage.all(State)
        obj_val = [value.to_dict() for value in objects.values()]
        return jsonify(obj_val)
    elif request.method == 'POST':
        try:
            content = request.get_json(force=True)
        except ValueError:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in content:
            return jsonify({'error': 'Missing name'}), 400

        new_state = State(**content)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_state_id(state_id):
    """
    Retrieves, deletes, or updates a State object by its ID.

    Methods:
        GET: Retrieves a State object by ID.
        DELETE: Deletes a State object by ID.
        PUT: Updates a State object by ID.

    Args:
        state_id (str): The ID of the State object.

    Returns:
        A JSON response with the State object or an appropriate status code.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            content = request.get_json(force=True)
        except ValueError:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, value in content.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
