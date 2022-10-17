import threading

import requests


class DiscoveryBalancer:
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"

    def __init__(self, discovery):
        self.discovery = discovery
        self.services = discovery.services["response"]
        self.node_counter = 0
        self.circuit_max = 5
        self.circuit_status = [500, 502, 503, 504]

    def __service_nodes_amount(self, service):
        return len(self.services[service])

    def circuit_resend(self, host, path, req, service):
        cur_error = 2  # first error was during client request
        while cur_error <= self.circuit_max:
            try:
                resp = self.__proxy_request(host, path, req)

                if resp.status_code not in self.circuit_status:
                    break
                else:
                    cur_error += 1
            except requests.exceptions.ConnectionError:
                cur_error += 1

        if cur_error - self.circuit_max == 1:
            self.discovery.detach(service, host)

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

        if resp.status_code in self.circuit_status:
            threading.Thread(target=self.circuit_resend,
                             args=[host, path, req]).start()

        return resp, resp.status_code
