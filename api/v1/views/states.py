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
            if 'name' not in content.keys():
                return 'Missing name', 400
            name_value = content['name']
            class_values = storage.all(State).values()
            for i in class_values:
                if name_value == i.to_dict()['name']:
                    return jsonify(i.to_dict()), 201
        except ValueError:
            return 'Nott a JSON', 400


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
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
    new = storage.all(State)
    key = 'State.' + state_id
    state = new.get(key)
    if state is None:
        abort(404)
    if request.method == 'GET':
        if state:
            return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        if state:
            del new[key]
            storage.save()
            return {}, 200
        else:
            abort(404)
    elif request.method == 'PUT':
        try:
            content = request.get_json()
            if not content:
                return 'Not a JSON', 400
            obj = storage.get(State, state_id)
            if obj is None:
                abort(404)
            for key, value in content.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        except ValueError:
            return 'Not a JSON', 400
