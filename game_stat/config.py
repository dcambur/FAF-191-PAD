from const import POSTGRES


class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://postgres:root@{POSTGRES}:5432/game_stat"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "some-key"
    DEBUG = False
