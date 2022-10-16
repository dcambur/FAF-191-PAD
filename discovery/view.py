from flask import Blueprint, request, jsonify
from discovery.registry import Registry

discovery = Blueprint("discovery", __name__, url_prefix="/discovery")
registry = Registry()


@discovery.route("get", methods=["GET"])
def get_service_list():
    return jsonify({"response": registry.services})


@discovery.route("register", methods=["POST"])
def register_service():
    data = request.get_json()
    resp = registry.register(data["service"], data["hostname"], data["endpoint"])

    return jsonify({"response": resp})