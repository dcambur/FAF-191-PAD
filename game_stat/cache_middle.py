import requests


class CacheMiddle:
    GAME = "game-"
    POPULARITY = "popularity-"
    LATEST_GAME = "latest-game-stats"

    def __init__(self, service_token="ceto-tam"):
        self.service_token = service_token
        self.headers = {"Authorization": "Bearer " + str(self.service_token)}
        self.POST = "http://127.0.0.1:5002/cache/post"
        self.GET = "http://127.0.0.1:5002/cache/get/"
        self.DELETE = "http://127.0.0.1:5002/cache/delete/"

    def send_game(self, game_id, body):
        requests.post(self.POST, json={f"{self.GAME}{game_id}": body},
                      headers=self.headers)
        return True

    def send_latest_games(self, body):
        requests.post(self.POST,
                      json={f"{self.LATEST_GAME}": body},
                      headers=self.headers)
        return True

    def receive_latest_games(self):
        return requests.get(self.GET + self.LATEST_GAME,
                            headers=self.headers).json()

    def receive_game(self, key):
        return requests.get(self.GET + f"{self.GAME}{key}",
                            headers=self.headers).json()

    def delete_game(self, key):
        return requests.delete(self.DELETE + f"{self.GAME}{key}",
                               headers=self.headers).json()
