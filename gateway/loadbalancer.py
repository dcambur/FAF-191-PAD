import requests


class DiscoveryBalancer:
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"

    def __init__(self, disc_resp):
        self.host = "host"
        self.services = disc_resp["response"]
        self.node_counter = 0

    def __service_nodes_amount(self, service):
        return len(self.services[service])

    def __proxy_request(self, host, path, req):
        if req.method == self.POST:
            return requests.post(host + path, data=req.data,
                                 headers=req.headers)
        if req.method == self.GET:
            return requests.get(host + path, headers=req.headers)
        if req.method == self.PUT:
            return requests.put(host + path, data=req.data,
                                headers=req.headers)
        if req.method == self.DELETE:
            return requests.delete(host + path, headers=req.headers)

    def round_robin(self, service, path, req):
        total_nodes = self.__service_nodes_amount(service)

        if self.node_counter == total_nodes:
            self.node_counter = 0

        host = self.services[service][self.node_counter]
        resp = self.__proxy_request(host, path, req)
        self.node_counter += 1

        return resp, resp.status_code
