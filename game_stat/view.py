import sqlalchemy.exc
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from const import SERVER_PORT, SERVER_HOST, FRAMEWORK_NAME
from model import Game, db, Popularity

game_stat = Blueprint("game_stat", __name__, url_prefix="/game")


@game_stat.route("get/latest", methods=["GET"])
def get_latest_games():
    games = Game.query.order_by(Game.created_at.desc()).limit(10).all()
    resp = []
    for game in games:
        resp.append(game.response())

    return jsonify({"response": resp}), 200


@game_stat.route("get/<int:game_id>", methods=["GET"])
def get_game_by_id(game_id):
    game = Game.query.filter_by(id=game_id).first()

    if not game:
        return jsonify({"response": "id doesn't exist"}), 409

    return jsonify({"response": game.response()}), 200


@game_stat.route("like/<int:game_id>", methods=["GET"])
@jwt_required()
def like_game(game_id):
    identity = get_jwt_identity()
    popularity = Popularity.query.filter_by(user_id=identity["id"]).first()

    if popularity:
        popularity.is_like = not popularity.is_like
    else:
        popularity = Popularity()
        popularity.game_id = game_id
        popularity.is_like = True
        popularity.user_id = identity["id"]

    db.session.add(popularity)
    db.session.commit()

    return jsonify({"response": "like/dislike success"}), 200


@game_stat.route("rating/get/<int:game_id>", methods=["GET"])
@jwt_required()
def get_rating(game_id):
    dislike = Popularity.query.filter_by(game_id=game_id, is_like=False).count()
    like = Popularity.query.filter_by(game_id=game_id, is_like=True).count()

    return jsonify({"response": (like - dislike) / (like + dislike)}), 200


@game_stat.route("dislike/get/all/<int:game_id>", methods=["GET"])
@jwt_required()
def get_dislikes(game_id):
    dislike = Popularity.query.filter_by(game_id=game_id, is_like=False).count()

    return jsonify({"response": dislike}), 200


@game_stat.route("like/get/all/<int:game_id>", methods=["GET"])
@jwt_required()
def get_likes(game_id):
    like = Popularity.query.filter_by(game_id=game_id, is_like=True).count()

    return jsonify({"response": like}), 200


@game_stat.route("post", methods=["POST"])
def post_game():
    try:
        game = Game()
        game.title = request.get_json()["title"]
        game.desc = request.get_json()["desc"]
        db.session.add(game)
        db.session.commit()
    except KeyError:
        return jsonify({"response": "[field], [desc] are required"}), 400
    except sqlalchemy.exc.IntegrityError:
        return jsonify({"response": "unique field violation"}), 409

    return jsonify({"response": "game post success"}), 200


@game_stat.route("update/<int:game_id>", methods=["PUT"])
def update_game(game_id):
    game = Game.query.filter_by(id=game_id).first()

    if game is None:
        return jsonify({"response": "id doesn't exist"}), 409
    try:
        game.title = request.get_json()["title"]
        game.dest = request.get_json()["desc"]

        db.session.add(game)
        db.session.commit()
    except KeyError:
        return jsonify({"response": "[field], [desc] are required"}), 400
    except sqlalchemy.exc.IntegrityError:
        return jsonify({"response": "unique field violation"}), 409

    return jsonify({"response": "game update success"}), 200


@game_stat.route("delete/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    game = Game.query.filter_by(id=game_id).first()

    if game is None:
        return jsonify({"response": "id doesn't exist"}), 409

    db.session.delete(game)
    db.session.commit()

    return jsonify({"response": "game delete success"}), 200


@game_stat.route("get/status", methods=["GET"])
def get_status():
    return jsonify({
        "port": SERVER_PORT,
        "host": SERVER_HOST,
        "addr": f"http://{SERVER_HOST}:{SERVER_PORT}/",
        "web-framework": FRAMEWORK_NAME,
    })
