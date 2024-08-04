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
    if state_id is NULL:
	
