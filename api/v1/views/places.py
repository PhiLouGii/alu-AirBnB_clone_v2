#!/usr/bin/python3
"""a new view for Place objects that handles all default RESTFul API actions"""

from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views

def getcity(city_id):
    """Return states"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = storage.all(Place).values()
    return jsonify([place.to_dict()
                    for place in places if place.city_id == city_id]), 200


@app_views.route('/places/<place_id>', strict_slashes=False)
def getplace(place_id):
    """return state"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteplace(place_id):
    """deletes"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def postplace(city_id):
    """creates place"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    # check if the user id provided in the request is linked to a User
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def putplace(place_id):
    """PUT"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
