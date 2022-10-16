from flask import Flask


def create_app():
    app = Flask(__name__)

    from view import discovery
    app.register_blueprint(discovery)

    return app
