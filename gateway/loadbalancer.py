import requests
from requests import request


class DiscoveryBalancer:
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"

    def __init__(self, disc_resp):
        self.host = "host"
        self.uri_list = "uri_list"
        self.services = disc_resp["response"]
        self.node_counter = 0
        self.http404 = "No such URL was found"

    def __service_nodes_amount(self, service):
        return len(self.services[service])

    def __proxy_request(self, host, path, req):
        if req.method == self.POST:
            return requests.post(host + path, data=req.data,
                                 headers=req.headers).json()
        if req.method == self.GET:
            return requests.get(host + path, headers=req.headers).json()
        if req.method == self.PUT:
            return requests.put(host + path, data=req.data,
                                headers=req.headers).json()
        if req.method == self.DELETE:
            return requests.delete(host + path, headers=req.headers).json()

    def round_robin(self, service, path, req):
        total_nodes = self.__service_nodes_amount(service)

        if self.node_counter == total_nodes:
            self.node_counter = 0

        host = self.services[service][str(self.node_counter)][self.host]
        uri = self.services[service][str(self.node_counter)][self.uri_list]
        if path in uri:
            print(f"proxying to {host}[id={self.node_counter}] on {path}")
            resp = self.__proxy_request(host, path, req)
        else:
            return self.http404, 404

        self.node_counter += 1

        return resp, 200
