from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config

jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    jwt.init_app(app)
    from view import auth
    app.register_blueprint(auth)

    return app
