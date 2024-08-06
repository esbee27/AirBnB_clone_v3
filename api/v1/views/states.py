#!/usr/bin/python3

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
import json


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_state():
    if request.method == 'GET':
        objects = storage.all(State)
        obj_val = [value.to_dict() for value in objects.values()]
        return jsonify(obj_val)
    elif request.method == 'POST':
        try:
            content = request.get_json(force=True)
            # data = json.loads(content)
            if 'name' not in content.keys():
                return 'Missing name', 400
            name_value = content['name']
            class_values = storage.all(State).values()
            for i in class_values:
                if name_value == i.to_dict()['name']:
                    return jsonify(i.to_dict()), 201
        except ValueError:
            return 'Not a JSON', 400


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_state_id(state_id):
    new = storage.all(State)
    key = 'State.' + state_id
    state = new.get(key)
    if request.method == 'GET':
        if state:
            return jsonify(state.to_dict())
        else:
            abort(404)
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
