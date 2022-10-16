from flask import Blueprint, request, jsonify
from registry import Registry

discovery = Blueprint("discovery", __name__, url_prefix="/discovery")
registry = Registry()


@discovery.route("get", methods=["GET"])
def get_service_list():
    return jsonify({"response": registry.services})


@discovery.route("register", methods=["PUT"])
def register_service():
    data = request.get_json()
    resp = registry.register(data["service"], data["hostname"])

    return jsonify({"response": resp})
