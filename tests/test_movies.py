import json
from datetime import date
import pytest
from src.castingagency.api.models.movie import Movie


def test_add_movie(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/movies",
        data=json.dumps(
            {"title": "He Got Game", "release_date": "1998-04-28"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert True == data['success']
    assert "He Got Game was added!" == data["message"]


def test_add_movie_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post("/movies", data=json.dumps({}),
                       content_type="application/json",)
    data = json.loads(resp.data.decode())
    assert resp.status_code == 422
    assert "unprocessable" == data["message"]


def test_get_single_movie(test_app, test_database, add_movie):
    movie = add_movie('Love and Basketball', date(1998, 4, 28))
    client = test_app.test_client()
    resp = client.get(f'/movies/{movie.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data['movies']) == 1
    assert 'Love and Basketball' == data['movies'][0]['title']
    assert '1998-04-28' == data['movies'][0]['release_date']


def test_get_all_movies(test_app, test_database, add_movie):
    test_database.session.query(Movie).delete()
    add_movie('He Got Game', date(1998, 4, 28))
    add_movie('He Got Game', date(1998, 4, 28))
    client = test_app.test_client()
    resp = client.get('/movies')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data['movies']) == 2
    assert 'He Got Game' == data['movies'][0]['title']
    assert "1998-04-28" == data['movies'][0]['release_date']
    assert 'He Got Game' == data['movies'][1]['title']
    assert "1998-04-28" == data['movies'][1]['release_date']


def test_remove_movie(test_app, test_database, add_movie):
    test_database.session.query(Movie).delete()
    movie = add_movie('He Got Game', date(1998, 4, 28))
    client = test_app.test_client()
    resp_one = client.get("/movies")
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data['movies']) == 1
    resp_two = client.delete(f"/movies/{movie.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert '1 was deleted!' in data["message"]
    resp_three = client.get("/movies")
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    print(data)
    assert len(data['movies']) == 0


def test_remove_actor_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/movies/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "Movie 999 does not exist" in data["message"]


def test_update_actor(test_app, test_database, add_movie):
    movie = add_movie('He Got Game', date(1998, 4, 28))
    client = test_app.test_client()
    resp_one = client.patch(
        f"/movies/{movie.id}",
        data=json.dumps({"title": "jamaal"}),
        content_type="application/json",
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert f"{movie.id} was updated!" in data["message"]
    resp_two = client.get(f"/movies/{movie.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "jamaal" in data['movies'][0]['title']
    assert "1998-04-28" == data['movies'][0]['release_date']
