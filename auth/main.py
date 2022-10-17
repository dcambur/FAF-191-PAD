from flask import Flask
from flask_jwt_extended import JWTManager

from const import SERVICE_NAME, SERVER_FULL
from discovery_middle import DiscoveryMiddleware
from config import Config

jwt = JWTManager()
discovery = DiscoveryMiddleware()


def create_app():
    app = Flask(__name__)
    discovery.send_register(SERVICE_NAME, SERVER_FULL)
    app.config.from_object(Config)
    jwt.init_app(app)
    from view import auth
    app.register_blueprint(auth)

    return app
