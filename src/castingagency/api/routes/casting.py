from flask import Blueprint, request
from flask_restx import Resource, Api
from src.castingagency.api.models.cast import CastSchema, casts
from sqlalchemy import insert

casts_blueprint = Blueprint('casts', __name__)
api = Api(casts_blueprint)

class CastsList(Resource):


    def post(self):
        try:
            post_data = request.get_json()
            print(post_data)
            cast = CastSchema().load(post_data, partial=True)
            print(cast)
            casts.insert().values(cast)

            # Actor(name=actor.name, age=actor.age, gender=actor.gender).insert()
            response_object = {
                'success': True,
                'message': f'1was added!'
            }
            return response_object, 201
        except:
            api.abort(422, succcess=False, message="unprocessable")

api.add_resource(CastsList, '/casts')