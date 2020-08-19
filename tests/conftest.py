import pytest
import requests
import json
import os

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

@pytest.fixture(scope='session')
def get_access_token():
    url = "https://jamaalsanders.auth0.com/oauth/token"
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    headers = {
        'content-type': 'application/json'
    }
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": "casting-agency",
        "grant_type": "client_credentials"
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(response.status_code)
    data = json.loads(response.text.encode("utf-8"))
    return data
