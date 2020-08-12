import os
from sqlalchemy import Column, String, Integer, Table, ForeignKey, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import post_load
from src.castingagency import db, ma


# db = SQLAlchemy()
# ma =

# def setup_db(app):
#     app.config["SQLALCHEMY_DATABASE_URI"] = database_path
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.app = app
#     db.init_app(app)
#     db.create_all()
#     ma = Marshmallow(app)
#
#
# def db_drop_and_create_all():
#     """drops the database tables and starts fresh
#     can be used to initialize a clean database"""
#     db.drop_all()
#     db.create_all()


# movie_actor = Table('movie_actor', db.Model.metadata,
#                     Column('movie_id', Integer, ForeignKey('movies.id')),
#                     Column('actor_id', Integer, ForeignKey('actors.id')))


# class Cast(db.Model):
#     __tablename__ = 'casts'
#     id = Column(Integer, primary_key=True)
#     movie_id = Column(Integer, ForeignKey('movie.id'))
#     actor_id = Column(Integer, ForeignKey('actor.id'))
#     movie = relationship("Movie", backref=backref("casts", cascade="all, delete-orphan"))
#     actor = relationship("Actor", backref=backref("casts", cascade="all, delete-orphan"))
#
#     def insert(self):
#         db.session.add(self)
#         db.session.commit()
#
#     def update(self):
#         db.session.commit()
#
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
#
#
# class CastSchema(ma.SQLAlchemyAutoSchema):
#
#     class Meta:
#         model = Cast
#         load_instance = True


