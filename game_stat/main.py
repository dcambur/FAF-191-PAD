from flask import Flask
from config import Config
from flask_migrate import Migrate
from model import db

migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate.init_app(app, db)
    from view import game_stat
    app.register_blueprint(game_stat)

    return app
