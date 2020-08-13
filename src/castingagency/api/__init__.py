from flask_restx import Api

from src.castingagency.api.routes.ping import ping_namespace
from src.castingagency.api.routes.actors import actor_namespace
from src.castingagency.api.routes.movies import movie_namespace


api = Api(version="1.0", title="Casting Agency API", doc="/doc/")

api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(actor_namespace, path="/actors")
api.add_namespace(movie_namespace, path="/movies")
