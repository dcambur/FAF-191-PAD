import datetime
import sqlalchemy.exc
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from const import SERVER_PORT, SERVER_HOST, FRAMEWORK_NAME, SERVER_FULL, \
    SERVICE_NAME
from identity import UserIdentity
from model import Game, db, Popularity
from cache_middle import CacheMiddleware

game_stat = Blueprint(SERVICE_NAME, __name__, url_prefix="/game")
cache_middle = CacheMiddleware()


@game_stat.route("get/latest/<int:max_num>", methods=["GET"])
def get_latest_games(max_num):
    games = Game.query.order_by(Game.modified_at.desc()).limit(max_num).all()
    resp = []

    for game in games:
        resp.append(game.response())

    return jsonify({"response": resp}), 200


@game_stat.route("get/<int:game_id>", methods=["GET"])
def get_game_by_id(game_id):
    cache = cache_middle.receive_game(game_id)

    if cache is not None:
        return jsonify({"response": cache}), 200

    game = Game.query.filter_by(id=game_id).first()
    if not game:
        return jsonify({"response": "id doesn't exist"}), 409

    cache_middle.send_game(game_id, game.response())

    return jsonify({"response": game.response()}), 200


@game_stat.route("like/<int:game_id>", methods=["GET"])
@jwt_required()
def like_game(game_id):
    cache = cache_middle.receive_game(game_id)

    if cache is None:
        game = Game.query.filter_by(id=game_id).first()
        if not game:
            return jsonify({"response": "game id does not exist"}), 409

    identity = UserIdentity(get_jwt_identity())
    popularity = Popularity.query.filter_by(user_id=identity.id).first()

    if popularity:
        popularity.is_like = not popularity.is_like
    else:
        popularity = Popularity()
        popularity.modified_at = datetime.datetime.now()
        popularity.game_id = game_id
        popularity.is_like = True
        popularity.user_id = identity.id

    db.session.add(popularity)
    db.session.commit()

    likes = popularity.get_likes(game_id)
    dislikes = popularity.get_dislikes(game_id)
    total = likes + dislikes

    cache["likes"] = Popularity().get_likes(game_id)
    cache["dislikes"] = Popularity().get_dislikes(game_id)
    cache["rating"] = (likes - dislikes) / total if total != 0 else 0
    cache_middle.send_game(game_id, cache)

    return jsonify({"response": "like/dislike succeed"}), 200


@game_stat.route("post", methods=["POST"])
def post_game():
    json_data = request.get_json()
    try:
        game = Game()
        game.update(json_data)
        cache_middle.send_game(game.id, game.response())
    except sqlalchemy.exc.IntegrityError:
        return jsonify({"response": "field violation"}), 409

    return jsonify({"response": game.response()}), 200


@game_stat.route("update/<int:game_id>", methods=["PUT"])
def update_game(game_id):
    json_data = request.get_json()
    cache = cache_middle.receive_game(game_id)

    if cache:
        try:
            game = Game.query.get(cache["id"])
            game.update(json_data)
            cache_middle.send_game(game_id, game.response())
        except sqlalchemy.exc.IntegrityError:
            return jsonify({"response": "field violation"}), 409
        return jsonify({"response": game.response()}), 200

    game = Game.query.filter_by(id=game_id).first()

    if game is None:
        return jsonify({"response": "game doesn't exist"}), 409
    try:
        game.update(json_data)
        cache_middle.send_game(game_id, game.response())
    except sqlalchemy.exc.IntegrityError:
        return jsonify({"response": "field violation"}), 409
    return jsonify({"response": game.response()}), 200


@game_stat.route("delete/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    cache = cache_middle.receive_game(game_id)

    if cache is not None:
        game = Game.query.get(cache["id"])
    else:
        game = Game.query.filter_by(id=game_id).first()

    if game is None:
        return jsonify({"response": "game doesn't exist"}), 409

    game.delete()
    cache_middle.delete_game(game_id)

    return jsonify({"response": "game delete success"}), 200


@game_stat.route("get/status", methods=["GET"])
def get_status():
    return jsonify({
        "port": SERVER_PORT,
        "host": SERVER_HOST,
        "addr": SERVER_FULL,
        "web-framework": FRAMEWORK_NAME,
    })
