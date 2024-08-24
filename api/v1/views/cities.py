#!/usr/bin/python3
"""
RestFull API for City
    retrive : GET /api/v1/states/<state_id>/cities
    retrive : GET /api/v1/cities/<city_id>
    delete : DELETE /api/v1/cities/<city_id>
    create : POST /api/v1/states/<state_id>/cities
    update : PUT /api/v1/cities/<city_id>
"""
from models.city import City
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage


@app_views.route("/states/<string:state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def retrive_cities(state_id):
    """retrive all state"""
    retrive = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for cities in state.cities:
        retrive.append(cities.to_dict())
    return jsonify(retrive)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """get city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a city based on its city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """create a new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs = request.get_json()
    kwargs['state_id'] = state_id
    city = City(**kwargs)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """update a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, attr, val)
    city.save()
    return jsonify(city.to_dict())
