from flask_restx import Api

from src.castingagency.api.routes.actors import actor_namespace
from src.castingagency.api.routes.movies import movie_namespace
from src.castingagency.auth.auth import AuthError


api = Api(version="1.0", title="Casting Agency API", doc="/docs",
          description="Udacity Casting Agency API that provided details on movies and actors that the agency"
                      " has produced.", contact="Jamaal Sanders",
          contact_email="jamaal.sanders@gmail.com")

# AuthError exceptions raised by the @requires_auth(permission) decorator method
@api.errorhandler(AuthError)
def auth_error(auth_error):
    print(auth_error)
    return {'message': auth_error.error['description'], 'success': False}, auth_error.status_code

api.add_namespace(actor_namespace, path="/actors")
api.add_namespace(movie_namespace, path="/movies")
