import datetime
import json

import sqlalchemy.exc
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from const import SERVER_PORT, SERVER_HOST, FRAMEWORK_NAME
from model import Game, db, Popularity
from cache_middle import CacheMiddle, update_maps

game_stat = Blueprint("game_stat", __name__, url_prefix="/game")
cache_middle = CacheMiddle()


@game_stat.route("get/latest/<int:max_num>", methods=["GET"])
def get_latest_games(max_num):
    cache = cache_middle.receive("latest-game-stats")
    if cache:
        return jsonify({"response": cache}), 200

    games = Game.query.order_by(Game.modified_at.desc()).limit(max_num).all()
    resp = []
    for game in games:
        resp.append(game.response())
    cache_middle.send({"latest-game-stats": resp})
    return jsonify({"response": resp}), 200


@game_stat.route("get/<int:game_id>", methods=["GET"])
def get_game_by_id(game_id):
    cache = cache_middle.receive(f"game-{game_id}")
    if cache is not None:
        return jsonify({"response": cache}), 200

    game = Game.query.filter_by(id=game_id).first()
    if not game:
        return jsonify({"response": "id doesn't exist"}), 409

    cache_middle.send({f"game-{game.id}": game.response()})

    return jsonify({"response": game.response()}), 200


@game_stat.route("like/<int:game_id>", methods=["GET"])
@jwt_required()
def like_game(game_id):
    cache = cache_middle.receive(f"game-{game_id}")
    if not cache:
        game = Game.query.filter_by(id=game_id).first()

        if not game:
            return jsonify({"response": "game id does not exist"}), 409

    identity = get_jwt_identity()
    popularity = Popularity.query.filter_by(user_id=identity["id"]).first()

    if popularity:
        popularity.is_like = not popularity.is_like
    else:
        popularity = Popularity()
        popularity.modified_at = datetime.datetime.now()
        popularity.game_id = game_id
        popularity.is_like = True
        popularity.user_id = identity["id"]

    db.session.add(popularity)
    db.session.commit()

    likes = popularity.get_likes(game_id)
    dislikes = popularity.get_dislikes(game_id)
    total = likes + dislikes

    cache["likes"] = Popularity().get_likes(game_id)
    cache["dislikes"] = Popularity().get_dislikes(game_id)
    cache["rating"] = (likes - dislikes) / total if total != 0 else 0

    cache_middle.send({f"game-{game_id}": cache})

    return jsonify({"response": "like/dislike succeed"}), 200


@game_stat.route("post", methods=["POST"])
def post_game():
    try:
        game = Game()
        game.title = request.get_json()["title"]
        game.desc = request.get_json()["desc"]
        db.session.add(game)
        db.session.commit()

        cache_middle.send({f"game-{game.id}": game.response()})
    except KeyError:
        return jsonify({"response": "[field], [desc] are required"}), 400
    except sqlalchemy.exc.IntegrityError:
        return jsonify({"response": "unique field violation"}), 409

    return jsonify({"response": game.response()}), 200


@game_stat.route("update/<int:game_id>", methods=["PUT"])
def update_game(game_id):
    cache = cache_middle.receive(f"game-{game_id}")

    if cache is not None:
        return jsonify({"response": cache}), 200

    game = Game.query.filter_by(id=game_id).first()

    if game is None:
        return jsonify({"response": "id doesn't exist"}), 409
    try:
        game.title = request.get_json()["title"]
        game.desc = request.get_json()["desc"]
        game.modified_at = datetime.datetime.now()
        db.session.add(game)
        db.session.commit()

        cache_middle.send({f"game-{game_id}": game.response()})
    except KeyError:
        return jsonify({"response": "[field], [desc] are required"}), 400
    except sqlalchemy.exc.IntegrityError:
        return jsonify({"response": "unique field violation"}), 409

    return jsonify({"response": game.response()}), 200


@game_stat.route("delete/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    cache = cache_middle.receive(f"game-{game_id}")

    if cache is not None:
        game = Game.query.get(cache["id"])
    else:
        game = Game.query.filter_by(id=game_id).first()

    if game is None:
        return jsonify({"response": "id doesn't exist"}), 409

    db.session.delete(game)

    db.session.commit()

    cache_middle.delete(f"game-{game_id}")
    return jsonify({"response": "game delete success"}), 200


@game_stat.route("get/status", methods=["GET"])
def get_status():
    return jsonify({
        "port": SERVER_PORT,
        "host": SERVER_HOST,
        "addr": f"http://{SERVER_HOST}:{SERVER_PORT}/",
        "web-framework": FRAMEWORK_NAME,
    })
