#!/usr/bin/python3
""" Create a new view for Amenity objects """
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """
    lists all /amenities of Amenity object
    """
    amenities = storage.all(Amenity).values()
    list_of_amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(list_ofamenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)
    else:
        return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenity_delete(amenity_id):
    """
    Deletes a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save

        return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_create():
    """
    Creates a Amenity
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    kwarg = request.get_json()
    if 'name' not in kwarg:
        abort(400, "Missing name")

    amenity = Amenity(**kwarg)

    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def amenity_update(amenity_id):
    """
    Updates a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        if not request.get_json():
            abort(400, "Not a JSON")

        keys = request.get_json()

        keys_ignore = ['id', 'created_at', 'updated_at']

        for key, value in keys.items():
            if key not in keys_ignore:
                setattr(amenity, key, value)
            

        amenity.save()
        return jsonify(amenity.to_dict()), 200
