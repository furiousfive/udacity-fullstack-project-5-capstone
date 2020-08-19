from flask import request
from flask_restx import Resource, Namespace, fields
from src.castingagency.api.models.actor import Actor, ActorSchema
from src.castingagency.auth.auth import requires_auth

actor_namespace = Namespace("Actors", description='Actors')

actor_model = actor_namespace.model(
    "Actor",
    {
        "name": fields.String(description='Actor Name', example="Jamaal"),
        "age": fields.Integer(example=25),
        "gender": fields.String(example="M", enum=['M', 'F']),
    },
)


class ActorBody(fields.Raw):
    def format(self, value):
        return {'name': value.name, 'age': value.age, 'gender': value.gender}


class ActorsList(Resource):
    @actor_namespace.doc(params={'Authorization': {'in': 'header',
                                                   'description': 'Authorization: Bearer <access_token>'}})
    @actor_namespace.response(200,"Success")
    @actor_namespace.response(403, "Permission not found.")
    @requires_auth('get:actors')
    def get(self, jwt):
        """Get a list of all actors"""
        actors = ActorSchema().dump(Actor.query.all(), many=True)
        response_object = {
            'success': True,
            'actors': actors
        }
        return response_object, 200


    @actor_namespace.response(201, "<actor_name> was added!")
    @actor_namespace.response(403, "Permission not found.")
    @actor_namespace.response(404, "Actor <actor_id> does not exist")
    @actor_namespace.response(422, "unprocessable")
    @actor_namespace.expect(actor_model)
    @actor_namespace.doc(params={'Authorization': {'in': 'header',
                                                   'description': 'Authorization: Bearer <access_token>'}})
    @requires_auth('post:actor')
    def post(self, jwt):
        """Create an actor"""
        try:
            request.get_json().pop('permission', None)
            post_data = request.get_json()
            actor = ActorSchema().load(post_data)
            Actor(name=actor.name, age=actor.age, gender=actor.gender).insert()
            response_object = {
                'success': True,
                'message': f'{actor.name} was added!',
                'actor': {"name": actor.name,
                          "age": actor.age,
                          "gender": actor.gender}
            }
            return response_object, 201
        except:
            actor_namespace.abort(422, succcess=False, message="unprocessable")


class Actors(Resource):
    @actor_namespace.doc(params={'Authorization': {'in': 'header',
                                                   'description': 'Authorization: Bearer <access_token>'}})
    @actor_namespace.response(200,"Success")
    @actor_namespace.response(403, "Permission not found.")
    @actor_namespace.response(404, "Actor <actor_id> does not exist")
    @actor_namespace.response(422, "unprocessable")
    @requires_auth('get:actor')
    def get(self, jwt, actor_id):
        """Get details about a specific actor"""
        actor = ActorSchema().dump(Actor.query.get(actor_id))
        if not actor:
            actor_namespace.abort(404, success=False,
                                  message=f"Actor {actor_id} does not exist")
        response_object = {
            'success': True,
            'actor': actor
        }
        return response_object, 200

    @actor_namespace.response(200, "<actor_id> was updated!")
    @actor_namespace.response(403, "Permission not found.")
    @actor_namespace.response(404, "Actor <actor_id> does not exist")
    @actor_namespace.response(422, "unprocessable")
    @actor_namespace.doc(params={'Authorization': {'in': 'header',
                                                   'description': 'Authorization: Bearer <access_token>'}})
    @requires_auth('patch:actor')
    def patch(self, jwt, actor_id):
        """Update detials about a specific actor"""
        actor = Actor.query.get(actor_id)
        if not actor:
            actor_namespace.abort(404, f"Actor {actor_id} does not exist")
        try:
            request.get_json().pop('permission', None)
            body = request.get_json()
            actor = ActorSchema().load(body, instance=actor, partial=True)
            actor.update()
            response_object = {
                'success': True,
                'message': f'{actor.id} was updated!',
                'actor': {"id": actor.id,
                          "name": actor.name,
                          "age": actor.age,
                          "gender": actor.gender}
            }
            return response_object, 200
        except:
            actor_namespace.abort(422, succcess=False, message="unprocessable")

    @actor_namespace.doc(params={'Authorization': {'in': 'header',
                                                   'description': 'Authorization: Bearer <access_token>'}})
    @actor_namespace.response(200, "<actor_id> was deleted!")
    @actor_namespace.response(403, "Permission not found.")
    @actor_namespace.response(404, "Actor <actor_id> does not exist")
    @actor_namespace.response(422, "unprocessable")
    @requires_auth('delete:actor')
    def delete(self, jwt, actor_id):
        """Delete a specific actor"""
        actor = Actor.query.get(actor_id)
        if not actor:
            actor_namespace.abort(404, succcess=False,
                                  message=f"Actor {actor_id} does not exist")
        try:
            actor.delete()
            response_object = {
                'message': f'Actor id {actor.id}, {actor.name} was deleted!',
                'success': True
            }
            return response_object, 200
        except:
            actor_namespace.abort(422, succcess=False, message="unprocessable")


actor_namespace.add_resource(ActorsList, '')
actor_namespace.add_resource(Actors, '/<int:actor_id>')
