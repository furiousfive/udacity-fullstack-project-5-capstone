from flask import request
from flask_restx import Resource, Namespace, fields
from src.castingagency.api.models.movie import Movie, MovieSchema
from src.castingagency.auth.auth import requires_auth

movie_namespace = Namespace("Movies", description='Movies')

movie_model = movie_namespace.model(
    "Movie",
    {
        "title": fields.String(description='Actor Name', example="Jamaal"),
        "release_date": fields.Date(example="1998-04-04"),
    },
)


class MoviesList(Resource):
    @movie_namespace.doc(params={'Authorization': {'in': 'header',
                                                   'description': 'Authorization: Bearer <access_token>'}})
    @movie_namespace.response(200, "Success")
    @movie_namespace.response(401, "Unauthorized")
    @movie_namespace.response(403, "Permission not found.")
    @requires_auth('get:movies')
    def get(self, jwt):
        """Get a list of all movies"""
        movies = MovieSchema().dump(Movie.query.all(), many=True)
        response_object = {
            'success': True,
            'movies': movies
        }
        return response_object, 200
    @movie_namespace.doc(params={'Authorization': {'in': 'header',
                                                   'description': 'Authorization: Bearer <access_token>'}})
    @movie_namespace.response(201, "<movie_id> was updated!")
    @movie_namespace.response(401, "Unauthorized")
    @movie_namespace.response(403, "Permission not found.")
    @movie_namespace.response(422, "unprocessable")
    @movie_namespace.expect(movie_model)
    @requires_auth('post:movie')
    def post(self, jwt):
        """Create a movie"""
        try:
            request.get_json().pop('permission', None)
            post_data = request.get_json()
            movie = MovieSchema().load(post_data)
            Movie(title=movie.title, release_date=movie.release_date).insert()
            response_object = {
                'success': True,
                'message': f'{movie.title} was added!',
                'movie': {"title": movie.title,
                          "release_date": str(movie.release_date)}
            }
            return response_object, 201
        except:
            movie_namespace.abort(422, succcess=False, message="unprocessable")


class Movies(Resource):

    @movie_namespace.doc(params={'Authorization': {'in': 'header',
                                                   'description': 'Authorization: Bearer <access_token>'}})
    @movie_namespace.response(200, "Success")
    @movie_namespace.response(401, "Unauthorized")
    @movie_namespace.response(403, "Permission not found.")
    @movie_namespace.response(404, "Movie <movie_id> does not exist")
    @movie_namespace.response(422, "unprocessable")
    @requires_auth('get:movie')
    def get(self, jwt, movie_id):
        """Get details about a specific movie"""
        movie = MovieSchema().dump(Movie.query.get(movie_id))
        if not movie:
            movie_namespace.abort(404, success=False,
                                  message=f"User {movie_id} does not exist")
        response_object = {
            'success': True,
            'movie': movie
        }
        return response_object, 200

    @movie_namespace.doc(params={'Authorization': {'in': 'header',
                                                   'description': 'Authorization: Bearer <access_token>'}})
    @movie_namespace.expect(movie_model)
    @movie_namespace.response(200, "<movie_id> was updated!")
    @movie_namespace.response(401, "Unauthorized")
    @movie_namespace.response(403, "Permission not found.")
    @movie_namespace.response(404, "Movie <movie_id> does not exist")
    @movie_namespace.response(422, "unprocessable")
    @requires_auth('patch:movie')
    def patch(self, jwt, movie_id):
        """Update detials about a specific movie"""
        movie = Movie.query.get(movie_id)
        if not movie:
            movie_namespace.abort(404, f"Movie {movie_id} does not exist")
        try:
            request.get_json().pop('permission', None)
            body = request.get_json()
            movie = MovieSchema().load(body, instance=movie, partial=True)
            movie.update()
            response_object = {
                'success': True,
                'message': f'{movie.id} was updated!',
                'movie': {"id": movie.id,
                          "title": movie.title,
                          "release_date": str(movie.release_date)}
            }
            return response_object, 200
        except:
            movie_namespace.abort(422, succcess=False, message="unprocessable")

    @movie_namespace.doc(params={'Authorization': {'in': 'header',
                                                   'description': 'Authorization: Bearer <access_token>'}})
    @movie_namespace.response(200, "<movie_id> was removed!")
    @movie_namespace.response(401, "Unauthorized")
    @movie_namespace.response(403, "Permission not found.")
    @movie_namespace.response(404, "Movie <movie_id> does not exist")
    @movie_namespace.response(422, "unprocessable")
    @requires_auth('delete:movie')
    def delete(self, jwt, movie_id):
        """Delete a specific movie"""
        movie = Movie.query.get(movie_id)
        if not movie:
            movie_namespace.abort(404, f"Movie {movie_id} does not exist")
        try:
            movie.delete()
            response_object = {
                'message': f'Movie id {movie.id}, {movie.title} was deleted!',
                'success': True
            }
            return response_object, 200
        except:
            movie_namespace.abort(422, succcess=False, message="unprocessable")


movie_namespace.add_resource(MoviesList, '')
movie_namespace.add_resource(Movies, '/<int:movie_id>')
