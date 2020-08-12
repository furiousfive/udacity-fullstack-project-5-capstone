from flask import Blueprint, request, jsonify
from flask_restx import Resource, Api

index_blueprint = Blueprint('index', __name__)
api = Api(index_blueprint)


class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }


api.add_resource(Ping, '/index')