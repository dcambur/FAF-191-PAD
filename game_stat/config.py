class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:root@127.0.0.1:5432/game_stat"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "some-key"
    DEBUG = True
