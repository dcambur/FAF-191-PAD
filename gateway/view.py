from flask import Blueprint, redirect, jsonify
from locator import DiscoveryServices

gateway = Blueprint("gateway", __name__, url_prefix="/")
discovery = DiscoveryServices()


@gateway.route('/', defaults={'path': ''})
@gateway.route('/<path:path>')
def route(path):
    services = discovery.services["response"]
    for service, hosts in services.items():
        for host, uri_list in hosts.items():
            for uri in uri_list:
                if path == uri:
                    return redirect(host + uri)
    return jsonify({"response": "404"}), 404
