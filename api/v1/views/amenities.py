#!/usr/bin/python3
"""
This module creates the view for all amenity objects
and handles all default api actions
"""

from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, String
import models

class Amenity(BaseModel, Base):
    """_summary_

    Args:
        BaseModel (_type_): _description_
        Base (_type_): _description_

    Returns:
        _type_: _description_
    """
    __tablename__ = 'amenities'
    
    if hasattr(models, 'storage_type') and models.storage_type == "db":
        name = Column(String(128), nullable=False)
    else:
        name = ""


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """
    This method retrieves all amenity objects
    Args: amenities - holds all amenity objects, keys excluded
    Return: json representation of dictionary
    """
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    This method retrieves one amenity object
    Args: amenity - contains one amenity object, based on its amenity id
          amenity_json - amenity object in dictionary format
    Return: json representation of dictionary
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity_json = amenity.to_dict()
        return jsonify(amenity_json)
    else:
        abort(404)  # Bad request


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    This method deletes an amenity object
    Args: amenity - contains one amenity object
    Return: empty dictionary
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return {}, 200  # OK
    else:
        abort(404)  # Bad request


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def create_amenity():
    """
    This method creates an amenity object
    Args: json_data - contains an HTTP body request to an amenity object
          amenity - contains one amenity object
          amenity_json - amenity object in dictionary format
    Return: json representation of dictionary
    """
    json_data = request.get_json(silent=True)
    if json_data:
        amenity = Amenity(**json_data)
        amenity.save()
        amenity_json = amenity.to_dict()
        return jsonify(amenity.to_dict()), 201
    elif "name" not in json_data:
        abort(400, "Missing name")  # Bad request
    else:
        abort(400, "Not a JSON")  # Bad request


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    This method updates an amenity object
    Args: json_data - contains an HTTP body request to an amenity object
    Return:
    """
    json_data = request.get_json(silent=True)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        storage.save()
        return jsonify(amenity_json), 200
    elif not json_data:
        abort(400, "Not a JSON")
            for key, value in json_data.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(amenity, key, value)
    else:
        abort(404)