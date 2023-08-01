#!/usr/bin/python3
"""holds endpoints for accessing Place objects"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route(
    '/cities/<city_id>/places/',
    methods=['GET', 'POST']
)
def all_places_endpoint(city_id):
    """Handles general requests for places in storage"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        places = storage.all(Place)
        place_list = []
        for place in places.values():
            if place.city_id == city.id:
                place_list.append(place.to_dict())
        return jsonify(place_list)
    if request.method == "POST":
        new_place_det = request.get_json(silent=True)
        if new_place_det is None:
            return "Not a JSON", 400
        if "user_id" not in new_place_det.keys():
            return "Missing user_id", 400
        if storage.get(User, new_place_det["user_id"]) is None:
            abort(404)
        if "name" not in new_place_det.keys():
            return "Missing name", 400
        new_place_det["city_id"] = city_id
        new_place = Place(**new_place_det)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route(
    '/places/<place_id>',
    methods=['GET', 'PUT', 'DELETE']
)
def place_endpoint(place_id):
    """Handles requests for a specific place in storage"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    if request.method == "PUT":
        new_det = request.get_json(silent=True)
        if new_det is None:
            return "Not a JSON", 400
        for key, val in new_det.items():
            if key not in ["id", "user_id", "city_id",
                           "created_at", "updated_at"]:
                setattr(place, key, val)
        place.save()
        return jsonify(place.to_dict())
    if request.method == "DELETE":
        place.delete()
        storage.save()
        return jsonify({})
