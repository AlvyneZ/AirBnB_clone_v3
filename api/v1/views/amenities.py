#!/usr/bin/python3
"""holds endpoints for accessing Amenity objects"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route(
    '/amenities/',
    methods=['GET', 'POST']
)
def all_amenities_endpoint():
    """Handles general requests for amenities in storage"""
    if request.method == "GET":
        amenities = storage.all(Amenity)
        amenity_list = []
        for amenity in amenities.values():
            amenity_list.append(amenity.to_dict())
        return jsonify(amenity_list)
    if request.method == "POST":
        new_amenity_det = request.get_json(silent=True)
        if new_amenity_det is None:
            return "Not a JSON", 400
        if "name" not in new_amenity_det.keys():
            return "Missing name", 400
        new_amenity = Amenity(**new_amenity_det)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET', 'PUT', 'DELETE']
)
def amenity_endpoint(amenity_id):
    """Handles requests for a specific amenity in storage"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "GET":
        return jsonify(amenity.to_dict())
    if request.method == "PUT":
        new_det = request.get_json(silent=True)
        if new_det is None:
            return "Not a JSON", 400
        for k, val in new_det.items():
            if (k != "id") and (k != "created_at") and (k != "updated_at"):
                setattr(amenity, k, val)
        amenity.save()
        return jsonify(amenity.to_dict())
    if request.method == "DELETE":
        amenity.delete()
        storage.save()
        return jsonify({})
