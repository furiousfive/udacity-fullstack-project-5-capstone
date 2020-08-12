import os
from sqlalchemy import Column, Integer, Table, ForeignKey
from marshmallow import Schema, fields
from src.castingagency import db, ma


class Casts(object):
    """
    Dogs object the "dogs" table.
    """
    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

casts = Table("casts",
             db.Model.metadata,
             Column('movie_id', Integer, ForeignKey('movies.id')),
             Column('actor_id', Integer, ForeignKey('actors.id'))
             )


class CastSchema(Schema):
    id = fields.Integer()
    movie_id = fields.Integer()
    actor_id = fields.Integer()


