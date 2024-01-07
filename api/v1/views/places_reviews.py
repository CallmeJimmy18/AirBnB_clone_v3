#!/usr/bin/python3
""" Create a new view for Review objects """
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
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
    review = storage.get(Review, review_idreview_id)

    if not review:
        abort(404)
    else:
        return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def review_delete(review_id):
    """
    Deletes a Review object
    """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)
    else:
        storage.delete(review)
        storage.save

        return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_create(place_id):
    """
    Creates a Review
    """
    placee = storage.get(Place, place_id)
    if not placee:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    kwarg = request.get_json()
    if 'user_id' not in kwarg:
        abort(400, "Missing user_id")

    if 'text' not in kwarg:
        abort(400, 'Missing text')

    user = storage.get(User, kwarg['user_id'])
    if not user:
        abort(404)

    kwarg['place_id'] = place_id
    review = Review(**kwarg)

    review.save()
    return jsonify(review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_update(review_id):
    """
    Updates a Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        if not request.get_json():
            abort(400, "Not a JSON")

        keys = request.get_json()

        keys_ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

        for key, value in keys.items():
            if key not in keys_ignore:
                setattr(review, key, value)
            

        review.save()
        return jsonify(review.to_dict()), 200
