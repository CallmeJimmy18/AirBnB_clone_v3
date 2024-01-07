#!/usr/bin/python3
""" Create a new view for City objects """
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """
    lists all cities of city object
    """
    states = storage.get(State, state_id)
    if not state:
        abort(404)

    list_of_cities = [city.to_dict() for city in states.cities]
    return jsonify(list_of_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id):
    """
    Deletes a City object
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save

        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_create(state_id):
    """
    Creates a City
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    kwarg = request.get_json()
    if 'name' not in kwarg:
        abort(400, "Missing name")

    kwarg['state_id'] = state_id
    city = City(**kwarg)

    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_update(city_id):
    """
    Updates a City object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        if not request.get_json():
            abort(400, "Not a JSON")

        keys = request.get_json()

        keys_ignore = ['id', 'state_id', 'created_at', 'updated_at']

        for key, value in keys.items():
            if key not in keys_ignore:
                setattr(city, key, value)

        city.save()
        return jsonify(city.to_dict()), 200
