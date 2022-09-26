import datetime

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Game(db.Model):
    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    title = db.Column(db.String, unique=True)
    desc = db.Column(db.String)
    likes = db.relationship("Popularity", back_populates="game")

    def response(self):
        return {"id": self.id,
                "created_at": self.created_at,
                "title": self.title,
                "desc": self.desc}


class Popularity(db.Model):
    __tablename__ = "popular"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    user = db.Column(db.Integer, nullable=False)
    is_like = db.Column(db.Boolean, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)
    game = db.relationship("Game", back_populates="likes")

    def response(self):
        return jsonify({"id": self.id,
                        "created_at": self.created_at,
                        "user": self.user,
                        "is_like": self.title,
                        "game_id": self.game_id})
