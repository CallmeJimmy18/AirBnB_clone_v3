#!/usr/bin/python3
""" Create a new view for State objects """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
    lists all stats of state object
    """
    states = storage.all(State).values()
    list_of_states = [state.to_dict() for state in states]
    return jsonify(list_of_states)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id):
    """
    Deletes a State object
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_create():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = State(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def state_update(state_id):
    """
    Updates a State object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    keys_ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in keys_ignore:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
