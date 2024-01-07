#!/usr/bin/python3
"""
Index of different routes
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Return API status
    """
    return jsonify(status="OK")


@app_views.route('/stats', method=['GET'])
def get_stats():
    """
    Return the object stats
    """
    statis = {
            "amenities": storage.count('Amenity'),
            "cities": storage.count('City'),
            "places": storage.count('Place'),
            "reviews": storage.count('Review'),
            "states": storage.count('State'),
            "users": storage.count('User')
            }

    return jsonify(statis)
