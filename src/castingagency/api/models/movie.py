import os
from sqlalchemy import Column, String, Integer, Table, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.castingagency import db, ma
from src.castingagency.api.models.cast import casts


class Movie(db.Model):
    """Movie model
    a movie must have a unique title
    a movie must also have a release_date
    """

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(80), nullable=False)
    release_date = Column(Date, nullable=False)
    actors = relationship("Actor", secondary=casts, backref=db.backref("movies", lazy="dynamic"))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return "<Author(name={self.name!r})>".format(self=self)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class MovieSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Movie
        load_instance = True
