#!/usr/bin/python3
""" Create a new view for State objects """
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/state', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
    lists all stats of state object
    """
    states = storage.all(State).values()
    list_of_states = [state.to_dict() for state in states]
    return jsonify(list_of_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    """
    Deletes a State object
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)
    else:
        storage.delete(state)
        storage.save

        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_create():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    kwarg = request.get_json()
    if 'name' not in kwarg:
        abort(400, "Missing name")

    state = State(**kwarg)

    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_update(state_id):
    """
    Updates a State object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        if not request.get_json():
            abort(400, "Not a JSON")

        keys = request.get_json()

        keys_ignore = ['id', 'created_at', 'updated_at']

        for key, value in keys.items():
            if key not in keys_ignore:
                setattr(state, key, value)

        state.save()
        return jsonify(state.to_dict()), 200
