from flask import Blueprint, jsonify, request
from pymongo import MongoClient

from const import SERVER_PORT, SERVER_HOST, FRAMEWORK_NAME
from flask_jwt_extended import create_access_token

auth = Blueprint("auth", __name__, url_prefix="/auth")

MONGODB_URI = "mongodb+srv://root:oNgy4iJcjqmaeR2M@cluster0.1dqchtj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)
auth_db = client["auth"]
user_collection = auth_db["user"]


@auth.route("login", methods=["POST"])
def login():
    username = request.get_json()["username"]

    if not username:
        return jsonify({"response": "username field is required"}), 409

    if not user_collection.find({"username": username}):
        return jsonify({"response": "user doesn't exist"})

    return jsonify(
        {"response": create_access_token(identity=username)}), 200


@auth.route("register", methods=["POST"])
def register():
    username = request.get_json()["username"]

    if not username:
        return jsonify({"response": "username field is required"}), 409

    if user_collection.find_one({"username": username}):
        return jsonify({"response": "user already exists"})

    user_collection.insert_one({"username": username})

    return jsonify(
        {"response": create_access_token(identity=username)}), 200


@auth.route("get/status", methods=["GET"])
def get_status():
    return jsonify({
        "port": SERVER_PORT,
        "host": SERVER_HOST,
        "addr": f"http://{SERVER_HOST}:{SERVER_PORT}/",
        "web-framework": FRAMEWORK_NAME,
    })
