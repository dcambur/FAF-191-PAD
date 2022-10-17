from flask import Blueprint, jsonify, request
from discovery_middle import DiscoveryMiddleware
from loadbalancer import DiscoveryBalancer

gateway = Blueprint("gateway", __name__, url_prefix="/")
discovery = DiscoveryMiddleware()
balancer = DiscoveryBalancer(discovery)


@gateway.route('/', defaults={'path': ''}, methods=["GET", "PUT", "POST", "DELETE"])
@gateway.route('/<path:path>', methods=["GET", "PUT", "POST", "DELETE"])
def route(path):
    service_name = path.split("/")[0]
    for service, _ in balancer.services.items():
        if service == service_name:
            [resp, status] = balancer.round_robin(service, path, request)
            if status == 200:
                return jsonify(resp.json()), status
            break

    return jsonify({"response": "URL Not Found"}), 404
