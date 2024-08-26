#!/usr/bin/python3
"""the app using flask to run on the:
    host = 0.0.0.0
    port= 50000
"""
from flask import Flask, Blueprint, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)

app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def handle(code):
    """close the storage at the end of req"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')

    app.run(host=host,
            port=port)
