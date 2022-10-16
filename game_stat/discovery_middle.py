import requests

from const import DISCOVERY


class RegisterData:

    def __init__(self, service, hostname):
        self.service = service
        self.hostname = hostname

    def to_dict(self):
        return {"service": self.service,
                "hostname": self.hostname}


class DiscoveryMiddleware:
    def __init__(self):
        self.__register = f"http://{DISCOVERY}:8002/discovery/register"

    def send_register(self, service, hostname):
        data = RegisterData(service, hostname).to_dict()
        requests.put(self.__register, json=data)
