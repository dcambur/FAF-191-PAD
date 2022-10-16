import os

SERVER_PORT = os.environ["SERVICE_PORT"]
SERVER_HOST = os.environ["SERVICE_NAME"]
SERVER_FULL = f"http://{SERVER_HOST}:{SERVER_PORT}/"
SERVICE_NAME = "game"
FRAMEWORK_NAME = "FLASK"
DISCOVERY = os.environ["DISCOVERY"]
CACHE = os.environ["CACHE"]
POSTGRES = os.environ["POSTGRES"]