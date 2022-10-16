
from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config
from flask_migrate import Migrate

from const import SERVICE_NAME, SERVER_FULL
from model import db
from discovery_middle import DiscoveryMiddleware

migrate = Migrate()
jwt = JWTManager()
discovery = DiscoveryMiddleware()


def create_app():
    app = Flask(__name__)
    discovery.send_register(SERVICE_NAME, SERVER_FULL)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    with app.app_context():
        db.create_all()

    migrate.init_app(app, db)
    from view import game_stat
    app.register_blueprint(game_stat)

    return app
