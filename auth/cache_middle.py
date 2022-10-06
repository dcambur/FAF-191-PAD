import requests


class CacheMiddle:
    def __init__(self, service_token="ceto-tam2"):
        self.service_token = service_token
        self.headers = {"Authorization": "Bearer " + str(self.service_token)}
        self.link = "http://cache:8001"
        self.POST = self.link + "/cache/post/"
        self.GET = self.link + "/cache/get/"
        self.DELETE = self.link + "/cache/delete/"

    def send(self, body):
        requests.post(self.POST, json=body,
                      headers=self.headers)
        return True

    def receive(self, key):
        return requests.get(self.GET + str(key),
                            headers=self.headers).json()

    def delete(self, key):
        return requests.delete(self.DELETE + str(key),
                               headers=self.headers).json()
