#!/usr/bin/python3
"""The module conatins the index for the api"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns the status of the api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def get_stats():
    """returns counts of the different objects"""
    from models import storage
    classes = {
            "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State,
            "users": User
            }
    return_dict = {}
    for key, cls in classes.items():
        # print({object})
        return_dict[key] = storage.count(cls)
    return jsonify(return_dict)
