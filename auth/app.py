from const import FLASK_HOST, FLASK_PORT
from main import create_app


if __name__ == "__main__":
    app = create_app()
    app.run(host=FLASK_HOST, port=FLASK_PORT)
