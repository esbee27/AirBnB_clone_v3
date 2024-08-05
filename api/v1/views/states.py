#!/usr/bin/python3
"""A view for State objects that handles all default RESTFul API actions
"""

@app_views.route("/states", methods='Get')
def list_states():
    """Lists all states"""
    list_states = [objt.to_dict() for objt in storage.all("State").values()]
    return jsonify(list_states)

@app_views.route("/states/<state_id>", methods='Get')
def get_state():
    """Retrieves a state object"""
    state = storage.get(State, state_id)
    if not state:
	abort(404)
    return jsonify(state.to_dict())

@app_views.route("/api/v1/states/<state_id>", methods='Delete')
def del_state():
    """Deletes state"""
    state = storage.get(State, state_id)
    if not state:
	abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)	

@app_views.route("/api/v1/states", methods='Post')
def update_state():
    """Creates a new state"""
    state = request.get_json('State')
    if not request.get_json():
	abort(404, description="Not a json")
    if 'name' is not in request.json():
	abort(404, description="Missing name")

@app_views.route("
    return make_response(jsonify(state.new(", 20)
