import pytest

from src.castingagency import create_app, db
from src.castingagency.api.models.actor import Actor
from src.castingagency.api.models.movie import Movie


@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object('src.castingagency.config.TestingConfig')
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    with app.app_context():
        yield app  # testing happens here


@pytest.fixture(scope='module')
def test_database():
    db.create_all()
    yield db  # testing happens here
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='function')
def add_actor():
    def _add_actor(name, age, gender):
        actor = Actor(name=name, age=age, gender=gender)
        db.session.add(actor)
        db.session.commit()
        return actor
    return _add_actor

@pytest.fixture(scope='function')
def add_movie():
    def _add_movie(title, release_date):
        movie = Movie(title=title, release_date=release_date)
        db.session.add(movie)
        db.session.commit()
        return movie
    return _add_movie