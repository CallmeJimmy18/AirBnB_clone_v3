#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """
    Close storage type
    """
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """
    handler for 404 errors
    """
    return jsonify(error="Not found")

if __name__ == "__main__":
    """ Main Function """
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host, int(port), threaded=True)
