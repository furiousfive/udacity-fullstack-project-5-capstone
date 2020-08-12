import os
from sqlalchemy import Column, Integer, Table, ForeignKey
from marshmallow import Schema, fields
from src.castingagency import db, ma

casts = Table("casts",
             db.Model.metadata,
             Column('movie_id', Integer, ForeignKey('movies.id')),
             Column('actor_id', Integer, ForeignKey('actors.id'))
             )


class CastSchema(Schema):
    id = fields.Integer()
    movie_id = fields.Integer()
    actor_id = fields.Integer()
