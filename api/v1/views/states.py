#!/usr/bin/python3
"""
RestFull API for State
    retrive : GET /api/v1/states
    delete : DELETE /api/v1/states/<state_id>
    create : POST /api/v1/states
    update : PUT /api/v1/states/<state_id>
"""
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def retrive():
    """retrive all state"""
    retrive = []
    for state in storage.all(State).values():
        retrive.append(state.to_dict())
    return jsonify(retrive)


@app_views.route("/states/<string:state_id>", methods=['GET'],
                 strict_slashes=False)
def retrive_by_id(state_id):
    """retrive state bised on the id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """delete a state using id"""
    """retrive state bised on the id"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    states.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create():
    """create new state param"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<string:state_id>", methods=['PUT'],
                 strict_slashes=False)
def ubdate(state_id):
    """update a state using id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, values in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, values)
    state.save()
    return jsonify(state.to_dict())
