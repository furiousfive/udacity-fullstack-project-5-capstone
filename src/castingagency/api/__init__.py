from flask_restx import Api

from src.castingagency.api.routes.actors import actor_namespace
from src.castingagency.api.routes.movies import movie_namespace


api = Api(version="1.0", title="Casting Agency API", doc="/docs",
          description="Hello World", contact="Jamaal Sanders",
          contact_email="jamaal.sanders@gmail.com")

api.add_namespace(actor_namespace, path="/actors")
api.add_namespace(movie_namespace, path="/movies")
