#!/usr/bin/python3
""" holds class User"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route(
    '/states/',
    methods=['GET', 'POST']
)
def all_states_endpoint():
    """Handles general requests for states in storage"""
    if request.method == "GET":
        states = storage.all(State)
        state_list = []
        for state in states.values():
            state_list.append(state.to_dict())
        return jsonify(state_list)
    if request.method == "POST":
        new_state_det = request.get_json(silent=True)
        if new_state_det is None:
            return "Not a JSON", 400
        if "name" not in new_state_det.keys():
            return "Missing name", 400
        new_state = State(**new_state_det)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route(
    '/states/<state_id>',
    methods=['GET', 'PUT', 'DELETE']
)
def state_endpoint(state_id):
    """Handles requests for a specific state in storage"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        return jsonify(state.to_dict())
    if request.method == "PUT":
        new_det = request.get_json(silent=True)
        if new_det is None:
            return "Not a JSON", 400
        for k, val in new_det.items():
            if (k != "id") and (k != "created_at") and (k != "updated_at"):
                setattr(state, k, val)
        state.save()
        return jsonify(state.to_dict())
    if request.method == "DELETE":
        state.delete()
        storage.save()
        return jsonify({})
