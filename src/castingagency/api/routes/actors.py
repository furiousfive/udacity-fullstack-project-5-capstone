from flask import Blueprint, request
from flask_restx import Resource, Api, fields
from src.castingagency.api.models.actor import Actor, ActorSchema


actors_blueprint = Blueprint('actors', __name__)
api = Api(actors_blueprint)


class ActorsList(Resource):

    def get(self):
        actors = ActorSchema().dump(Actor.query.all(), many=True)
        response_object = {
            'success': True,
            'actors': actors
        }
        return response_object, 200

    def post(self):
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
            api.abort(422, succcess=False, message="unprocessable")



class Actors(Resource):

    def get(self, actor_id):
        actor = ActorSchema().dump(Actor.query.get(actor_id))
        if not actor:
            api.abort(404, success=False,  message=f"User {actor_id} does not exist")
        response_object = {
            'success': True,
            'actors': [actor]
        }
        return response_object, 200


    def patch(self, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            api.abort(404, f"User {actor_id} does not exist")
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
            api.abort(422, succcess=False, message="unprocessable")



    def delete(self, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            api.abort(404, succcess=False, message=f"Actor {actor_id} does not exist")
        try:
            actor.delete()
            response_object = {
                 'message': f'{actor.id} was deleted!'
            }
            return response_object, 200
        except:
            api.abort(422, succcess=False, message="unprocessable")


api.add_resource(ActorsList, '/actors')
api.add_resource(Actors, '/actors/<int:actor_id>')
