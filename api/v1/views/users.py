#!/usr/bin/python3
"""holds endpoints for accessing User objects"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route(
    '/users/',
    methods=['GET', 'POST']
)
def all_users_endpoint():
    """Handles general requests for users in storage"""
    if request.method == "GET":
        users = storage.all(User)
        user_list = []
        for user in users.values():
            user_list.append(user.to_dict())
        return jsonify(user_list)
    if request.method == "POST":
        new_user_det = request.get_json(silent=True)
        if new_user_det is None:
            return "Not a JSON", 400
        if "email" not in new_user_det.keys():
            return "Missing email", 400
        if "password" not in new_user_det.keys():
            return "Missing password", 400
        new_user = User(**new_user_det)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route(
    '/users/<user_id>',
    methods=['GET', 'PUT', 'DELETE']
)
def user_endpoint(user_id):
    """Handles requests for a specific user in storage"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == "GET":
        return jsonify(user.to_dict())
    if request.method == "PUT":
        new_det = request.get_json(silent=True)
        if new_det is None:
            return "Not a JSON", 400
        for key, val in new_det.items(): 
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, key, val)
        user.save()
        return jsonify(user.to_dict())
    if request.method == "DELETE":
        user.delete()
        storage.save()
        return jsonify({})
