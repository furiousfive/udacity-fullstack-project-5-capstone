import json
import pytest
from src.castingagency.api.models.actor import Actor


def test_add_actor(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/actors",
        data=json.dumps({"name": "jamaal", "age": 37, "gender": "M"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert True == data['success']
    assert "jamaal was added!" == data["message"]


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post("/actors", data=json.dumps({}), content_type="application/json",)
    data = json.loads(resp.data.decode())
    assert resp.status_code == 422
    assert "unprocessable" == data["message"]

def test_get_single_actors(test_app, test_database, add_actor):
    actor = add_actor('jaimen', 33, 'M')
    client = test_app.test_client()
    resp = client.get(f'/actors/{actor.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data['actors']) == 1
    assert 'jaimen' == data['actors'][0]['name']
    assert 33 == data['actors'][0]['age']
    assert 'M' == data['actors'][0]['gender']


def test_get_all_actors(test_app, test_database, add_actor):
    test_database.session.query(Actor).delete()
    add_actor('jamaal', 37, 'M')
    add_actor('heather', 37, 'F')
    client = test_app.test_client()
    resp = client.get('/actors')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data['actors']) == 2
    assert 'jamaal' == data['actors'][0]['name']
    assert 37 == data['actors'][0]['age']
    assert 'M' == data['actors'][0]['gender']
    assert 'heather' == data['actors'][1]['name']
    assert 37 == data['actors'][1]['age']
    assert 'F' == data['actors'][1]['gender']


def test_remove_actor(test_app, test_database, add_actor):
    test_database.session.query(Actor).delete()
    actor = add_actor("jaimen", 25, 'M')
    client = test_app.test_client()
    resp_one = client.get("/actors")
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data['actors']) == 1
    resp_two = client.delete(f"/actors/{actor.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert '1 was deleted!'in data["message"]
    resp_three = client.get("/actors")
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data['actors']) == 0


def test_remove_actor_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/actors/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "Actor 999 does not exist" in data["message"]


def test_update_actor(test_app, test_database, add_actor):
    actor = add_actor("jaimen", 25, 'M')
    client = test_app.test_client()
    resp_one = client.patch(
        f"/actors/{actor.id}",
        data=json.dumps({"name": "jamaal"}),
        content_type="application/json",
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert f"{actor.id} was updated!" in data["message"]
    resp_two = client.get(f"/actors/{actor.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "jamaal" in data['actors'][0]['name']
    assert "M" in data['actors'][0]["gender"]
