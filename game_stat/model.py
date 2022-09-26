import datetime

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Game(db.Model):
    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.now())
    title = db.Column(db.String, unique=True)
    desc = db.Column(db.String)
    likes = db.relationship("Popularity", back_populates="game",
                            cascade="all,delete")

    def response(self):
        likes = Popularity().get_likes(self.id)
        dislikes = Popularity().get_dislikes(self.id)

        total = likes + dislikes
        return {"id": self.id,
                "modified_at": str(self.modified_at),
                "title": self.title,
                "likes": likes,
                "dislikes": dislikes,
                "rating": (likes - dislikes) / total if total != 0 else 0,
                "desc": self.desc}


class Popularity(db.Model):
    __tablename__ = "popular"

    id = db.Column(db.Integer, primary_key=True)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.String, unique=True, nullable=False)
    is_like = db.Column(db.Boolean, nullable=False)
    game_id = db.Column(db.Integer,
                        db.ForeignKey("game.id", ondelete="CASCADE"),
                        nullable=False)

    game = db.relationship("Game", back_populates="likes")

    def response(self):
        return jsonify({"id": self.id,
                        "modified_at": self.modified_at,
                        "user": self.user,
                        "is_like": self.title,
                        "game_id": self.game_id})

    def get_likes(self, game_id):
        return self.query.filter_by(game_id=game_id, is_like=True).count()

    def get_dislikes(self, game_id):
        return self.query.filter_by(game_id=game_id, is_like=False).count()

