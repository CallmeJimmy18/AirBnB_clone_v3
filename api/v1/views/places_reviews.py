#!/usr/bin/python3
""" Create a new view for Review objects """
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """
    lists all Reviews of Place object
    """
    places = storage.get(Place, place_id)

    if not places:
        abort(404)

    list_of_reviews = [reviews.to_dict() for reviews in places.reviews]
    return jsonify(list_of_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object
    """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    """
    Deletes a Review object
    """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_create(place_id):
    """
    Creates a Review
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    if 'text' not in request.get_json():
        abort(400, description='Missing text')

    data['place_id'] = place_id
    instance = Review(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_update(review_id):
    """
    Updates a Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    keys_ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in keys_ignore:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
