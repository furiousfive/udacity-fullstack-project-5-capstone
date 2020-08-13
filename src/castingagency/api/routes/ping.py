# from flask import Blueprint
from flask_restx import Resource, Namespace


ping_namespace = Namespace("ping")

# ping_blueprint = Blueprint('ping', __name__)
# api = Api(ping_blueprint)


class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }


ping_namespace.add_resource(Ping, '')