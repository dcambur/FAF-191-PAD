import requests


class DiscoveryServices:
    def __init__(self):
        self.url = "http://127.0.0.1:5000/discovery/get"
        self.services = self.__fetch().json()

    def __fetch(self):
        return requests.get(self.url)
