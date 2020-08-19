import json
from datetime import date
from src.castingagency.api.models.movie import Movie


def test_add_movie(test_app, test_database, get_access_token):
    client = test_app.test_client()
    access_token = get_access_token['access_token']
    resp = client.post(
        "/movies",
        headers={"Authorization": f"Bearer {access_token}"},
        data=json.dumps(
            {"title": "He Got Game", "release_date": "1998-04-28"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert True == data['success']
    assert "He Got Game was added!" == data["message"]


def test_add_movie_invalid_json(test_app, test_database, get_access_token):
    client = test_app.test_client()
    access_token = get_access_token['access_token']
    resp = client.post("/movies",
                       headers={"Authorization": f"Bearer {access_token}"},
                       data=json.dumps({}),
                       content_type="application/json",)
    data = json.loads(resp.data.decode())
    assert resp.status_code == 422
    assert "unprocessable" == data["message"]


def test_get_single_movie(test_app, test_database, add_movie, get_access_token):
    movie = add_movie('Love and Basketball', date(1998, 4, 28))
    client = test_app.test_client()
    access_token = get_access_token['access_token']
    resp = client.get(f'/movies/{movie.id}',
                      headers = {"Authorization": f"Bearer {access_token}"})
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data['movie']) == 3
    assert 'Love and Basketball' == data['movie']['title']
    assert '1998-04-28' == data['movie']['release_date']


def test_get_all_movies(test_app, test_database, add_movie, get_access_token):
    test_database.session.query(Movie).delete()
    add_movie('He Got Game', date(1998, 4, 28))
    add_movie('He Got Game', date(1998, 4, 28))
    client = test_app.test_client()
    access_token = get_access_token['access_token']
    resp = client.get('/movies',
                      headers={"Authorization": f"Bearer {access_token}"})
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data['movies']) == 2
    assert 'He Got Game' == data['movies'][0]['title']
    assert "1998-04-28" == data['movies'][0]['release_date']
    assert 'He Got Game' == data['movies'][1]['title']
    assert "1998-04-28" == data['movies'][1]['release_date']


def test_remove_movie(test_app, test_database, add_movie, get_access_token):
    test_database.session.query(Movie).delete()
    movie = add_movie('He Got Game', date(1998, 4, 28))
    client = test_app.test_client()
    access_token = get_access_token['access_token']
    resp_one = client.get("/movies",
                          headers={"Authorization": f"Bearer {access_token}"})
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data['movies']) == 1
    resp_two = client.delete(f"/movies/{movie.id}",
                             headers={"Authorization": f"Bearer {access_token}"})
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert f'Movie id {movie.id}, {movie.title} was deleted!' in data["message"]
    resp_three = client.get("/movies",
                            headers={"Authorization": f"Bearer {access_token}"})
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    print(data)
    assert len(data['movies']) == 0


def test_remove_actor_incorrect_id(test_app, test_database, get_access_token):
    client = test_app.test_client()
    access_token = get_access_token['access_token']
    resp = client.delete("/movies/999",
                         headers={"Authorization": f"Bearer {access_token}"})
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "Movie 999 does not exist" in data["message"]


def test_update_movie(test_app, test_database, add_movie, get_access_token):
    movie = add_movie('He Got Game', date(1998, 4, 28))
    client = test_app.test_client()
    access_token = get_access_token['access_token']
    resp_one = client.patch(
        f"/movies/{movie.id}",
        headers={"Authorization": f"Bearer {access_token}"},
        data=json.dumps({"title": "jamaal"}),
        content_type="application/json",
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert f"{movie.id} was updated!" in data["message"]
    resp_two = client.get(f"/movies/{movie.id}",
                          headers={"Authorization": f"Bearer {access_token}"})
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "jamaal" in data['movie']['title']
    assert "1998-04-28" == data['movie']['release_date']


def test_update_actor_incorrect_id(test_app, test_database, get_access_token):
    client = test_app.test_client()
    access_token = get_access_token['access_token']
    resp = client.patch("/movies/999",
                         headers={"Authorization": f"Bearer {access_token}"})
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "Movie 999 does not exist" in data["message"]