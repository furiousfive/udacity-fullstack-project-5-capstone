from flask import request
from flask_restx import Resource, Namespace, fields
from src.castingagency.api.models.actor import Actor, ActorSchema

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


# @actor_namespace.doc(model=actor_model,)
class ActorsList(Resource):

    @actor_namespace.doc(description='Hello World')
    def get(self):
        "Hello"
        actors = ActorSchema().dump(Actor.query.all(), many=True)
        response_object = {
            'success': True,
            'actors': actors
        }
        return response_object, 200

    @actor_namespace.doc(description='Hello World')
    @actor_namespace.expect(actor_model)
    def post(self):
        "Hello"
        try:
            post_data = request.get_json()
            actor = ActorSchema().load(post_data)
            Actor(name=actor.name, age=actor.age, gender=actor.gender).insert()
            response_object = {
                'success': True,
                'message': f'{actor.name} was added!'
            }
            return response_object, 201
        except:
            actor_namespace.abort(422, succcess=False, message="unprocessable")


class Actors(Resource):

    @actor_namespace.doc(description='Hello World')
    def get(self, actor_id):
        "Hello"
        actor = ActorSchema().dump(Actor.query.get(actor_id))
        if not actor:
            actor_namespace.abort(404, success=False,
                                  message=f"User {actor_id} does not exist")
        response_object = {
            'success': True,
            'actors': [actor]
        }
        return response_object, 200

    @actor_namespace.doc(description='Hello World')
    def patch(self, actor_id):
        "Hello"
        actor = Actor.query.get(actor_id)
        if not actor:
            actor_namespace.abort(404, f"User {actor_id} does not exist")
        try:
            body = request.get_json()
            actor = ActorSchema().load(body, instance=actor, partial=True)
            actor.update()
            response_object = {
                'success': True,
                'message': f'{actor.id} was updated!'
            }
            return response_object, 200
        except:
            actor_namespace.abort(422, succcess=False, message="unprocessable")

    @actor_namespace.doc(description='Hello World')
    def delete(self, actor_id):
        "Hello"
        actor = Actor.query.get(actor_id)
        if not actor:
            actor_namespace.abort(404, succcess=False,
                                  message=f"Actor {actor_id} does not exist")
        try:
            actor.delete()
            response_object = {
                'message': f'{actor.id} was deleted!'
            }
            return response_object, 200
        except:
            actor_namespace.abort(422, succcess=False, message="unprocessable")


actor_namespace.add_resource(ActorsList, '')
actor_namespace.add_resource(Actors, '/<int:actor_id>')
