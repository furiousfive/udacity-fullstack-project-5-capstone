from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship, backref
from src.castingagency import db, ma
from src.castingagency.api.models.cast import casts


class Actor(db.Model):
    """Actor model
    an actor must have a name, age and gender
    movies is a foreign key pointing to the movies the actor has been in
    """

    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(6), nullable=False)
    movies = relationship("Movie", secondary=casts, backref=db.backref("actor", lazy="dynamic"))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return '<Actor: {}>'.format(self.name)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ActorSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Actor
        load_instance = True