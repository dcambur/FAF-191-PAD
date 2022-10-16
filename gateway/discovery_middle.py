import requests

from const import DISCOVERY


class DiscoveryMiddleware:
    def __init__(self):
        self.url = f"http://{DISCOVERY}:8002/discovery/get"
        self.services = self.__fetch().json()

    def __fetch(self):
        return requests.get(self.url)
