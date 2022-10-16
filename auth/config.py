from datetime import timedelta


class Config:
    SECRET_KEY = "some-key"
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
