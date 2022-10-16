from flask import Flask


def create_app():
    app = Flask(__name__)
    app.debug = True

    from view import gateway
    app.register_blueprint(gateway)

    return app
