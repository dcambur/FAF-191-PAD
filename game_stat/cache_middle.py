import threading

import requests

from const import CACHE


class CacheMiddleware:
    GAME = "game-"
    POPULARITY = "popularity-"

    def __init__(self, service_token="ceto-tam"):
        self.service_token = service_token
        self.headers = {"Authorization": "Bearer " + str(self.service_token)}
        self.link = f"http://{CACHE}:8001"
        self.POST = self.link + "/cache/post"
        self.GET = self.link + "/cache/get/"
        self.DELETE = self.link + "/cache/delete/"

    def send_game(self, game_id, body):
        requests.post(self.POST, json={f"{self.GAME}{game_id}": body},
                      headers=self.headers)
        return True

    def receive_game(self, key):
        return requests.get(self.GET + f"{self.GAME}{key}",
                            headers=self.headers).json()

    def delete_game(self, key):
        return requests.delete(self.DELETE + f"{self.GAME}{key}",
                               headers=self.headers).json()
