import requests
from const import DISCOVERY


class DiscoveryMiddleware:
    def __init__(self):
        self.url = f"http://{DISCOVERY}:8002/discovery"
        self.get = "/get"
        self.delete = "/delete"
        self.services = self.__fetch().json()

    def __fetch(self):
        return requests.get(self.url + self.get)

    def detach(self, service, node_name):
        return requests.delete(f"{self.url}{self.delete}/{service}",
                               params={"node": node_name})
