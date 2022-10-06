from flask import Blueprint, jsonify, request
from pymongo import MongoClient

from cache_middle import CacheMiddle
from const import SERVER_PORT, SERVER_HOST, FRAMEWORK_NAME
from flask_jwt_extended import create_access_token

auth = Blueprint("auth", __name__, url_prefix="/auth")

MONGODB_URI = "mongodb+srv://root:NxXK98vXWtSEGcjF@cluster0.1dqchtj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)
auth_db = client["auth"]
user_collection = auth_db["user"]
cache_middle = CacheMiddle()


@auth.route("login", methods=["POST"])
def login():
    username = request.get_json()["username"]

    if not username:
        return jsonify({"response": "username field is required"}), 409

    cache = cache_middle.receive(f"identity-{username}")
    if cache is not None:
        return jsonify(
            {"response": create_access_token(identity=cache)}), 200

    cur_user = user_collection.find_one({"username": username})
    if not cur_user:
        return jsonify({"response": "user doesn't exist"})

    identity = {"id": str(cur_user["_id"]),
                "username": cur_user["username"]}
    cache_middle.send({f"identity-{username}": identity})

    return jsonify(
        {"response": create_access_token(identity=identity)}), 200


@auth.route("register", methods=["POST"])
def register():
    username = request.get_json()["username"]

    if not username:
        return jsonify({"response": "username field is required"}), 409

    if user_collection.find_one({"username": username}):
        return jsonify({"response": "user already exists"})

    user_data = {"username": username}
    user_collection.insert_one(user_data)

    cur_user = user_collection.find_one(user_data)
    identity = {"id": str(cur_user["_id"]),
                "username": cur_user["username"]}
    cache_middle.send({f"identity-{username}": identity})

    return jsonify(
        {"response": create_access_token(identity=identity)}), 200


@auth.route("get/status", methods=["GET"])
def get_status():
    return jsonify({
        "port": SERVER_PORT,
        "host": SERVER_HOST,
        "addr": f"http://{SERVER_HOST}:{SERVER_PORT}/",
        "web-framework": FRAMEWORK_NAME,
    })
