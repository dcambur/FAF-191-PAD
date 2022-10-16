from flask import Blueprint, redirect, jsonify, request
from discovery_fetch import DiscoveryFetcher
from gateway.loadbalancer import DiscoveryBalancer

gateway = Blueprint("gateway", __name__, url_prefix="/")
discovery = DiscoveryFetcher()
balancer = DiscoveryBalancer(discovery.services)


@gateway.route('/', defaults={'path': ''})
@gateway.route('/<path:path>')
def route(path):

    for service, _ in balancer.services.items():
        [resp, status] = balancer.round_robin(service, path, request)

        if status == 200:
            return jsonify(resp), status

    return "URL Not Found", 404

