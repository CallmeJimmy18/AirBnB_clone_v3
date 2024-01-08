#!/usr/bin/python3
""" Create a new view for Amenity objects """
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """
    lists all /amenities of Amenity object
    """
    amenities = storage.all(Amenity).values()
    list_of_amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(list_of_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """
    Deletes a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_create():
    """
    Creates a Amenity
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Amenity(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenity_update(amenity_id):
    """
    Updates a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    keys_ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in keys_ignore:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
