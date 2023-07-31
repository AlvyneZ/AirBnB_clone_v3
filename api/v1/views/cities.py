#!/usr/bin/python3
"""holds endpoints for accessing City objects"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route(
    '/states/<state_id>/cities/',
    methods=['GET', 'POST']
)
def all_cities_endpoint(state_id):
    """Handles general requests for cities in storage"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        cities = storage.all(City)
        city_list = []
        for city in cities.values():
            if city.state_id == state.id:
                city_list.append(city.to_dict())
        return jsonify(city_list)
    if request.method == "POST":
        new_city_det = request.get_json(silent=True)
        if new_city_det is None:
            return "Not a JSON", 400
        if "name" not in new_city_det.keys():
            return "Missing name", 400
        new_city_det["state_id"] = state.id
        new_city = City(**new_city_det)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route(
    '/cities/<city_id>',
    methods=['GET', 'PUT', 'DELETE']
)
def city_endpoint(city_id):
    """Handles requests for a specific city in storage"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify(city.to_dict())
    if request.method == "PUT":
        new_det = request.get_json(silent=True)
        if new_det is None:
            return "Not a JSON", 400
        for k, val in new_det.items():
            if (k != "id") and (k != "created_at") and (k != "updated_at"):
                setattr(city, k, val)
        city.save()
        return jsonify(city.to_dict())
    if request.method == "DELETE":
        city.delete()
        storage.save()
        return jsonify({})
