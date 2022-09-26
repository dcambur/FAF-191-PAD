import requests


def update_maps(map1, map2):
    for key, value in map1:
        if key in map2.keys():
            if map1[key] != map2[key]:
                map1[key] = map2[key]
    return map1


class CacheMiddle:
    def __init__(self, service_token="ceto-tam"):
        self.service_token = service_token
        self.headers = {"Authorization": "Bearer " + str(self.service_token)}
        self.POST = "http://127.0.0.1:5002/cache/post"
        self.GET = "http://127.0.0.1:5002/cache/get/"
        self.DELETE = "http://127.0.0.1:5002/cache/delete/"

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
