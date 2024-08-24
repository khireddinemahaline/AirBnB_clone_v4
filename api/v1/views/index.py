#!/usr/bin/python3
"""
route to api/v1/status
using the app_views Blueprint
* add some stats
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

HBNB_class = {
  "amenities": "Amenity",
  "cities": "City",
  "places": "Place",
  "reviews": "Review",
  "states": "State",
  "users": "User"
}


@app_views.route("/status", strict_slashes=False)
def return_ok():
    """return status code whene succsess"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def count():
    """count objs stored in the storage"""
    new_dic = {}
    for key, values in HBNB_class.items():
        new_dic[key] = storage.count(globals()[values])
    return jsonify(new_dic)
