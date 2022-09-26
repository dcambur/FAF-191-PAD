from datetime import timedelta


class Config:
    SECRET_KEY = "some-key"
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
