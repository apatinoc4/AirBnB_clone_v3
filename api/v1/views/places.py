#!/usr/bin/python3
"""
Cities file for APi project
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def show_places(city_id):
    """This functions lists all the places from a city"""
    list_t = []
    cities = storage.all("City")
    cityname = "City." + city_id
    if cities.get(cityname) is None:
        abort(404)
    else:
        places = storage.all("Place")
        for place in places.values():
            if place.city_id == city_id:
                list_t.append(place.to_dict())
    return jsonify(list_t)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """This functions get a specific place by its id"""
    places = storage.all("Place")
    placename = "Place." + place_id
    if cities.get(placename) is None:
        abort(404)
    place = places.get(placename).to_dict()
    return city


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """This function delete a place by its id"""
    places = storage.all('Place')
    placename = "Place." + place_id
    to_del = places.get(placename)
    if to_del is None:
        abort(404)
    storage.delete(to_del)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """This function create a new place"""
    data = request.get_json()
    cities = storage.all("City")
    match = "City." + city_id
    if cities.get(match) is None:
        abort(404)
    if not data:
        abort(400, 'Not a JSON')
    elif 'name' not in data:
        abort(400, 'Missing name')
    place = Place()
    place.name = data['name']
    place.city_id = city_id
    place.save()
    place = place.to_dict()
    return jsonify(place), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """This function update a place by id"""
    data = request.get_json()
    places = storage.all('Place')
    match = 'Place.' + place_id
    if places.get(match) is None:
        abort(404)
    if not data:
        abort(400, 'Not a JSON')
    else:
        place = places.get(match)
        place.name = data['name']
        place.save()
        place = place.to_dict()
    return jsonify(place), 200
