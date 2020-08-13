from flask import request
from flask_restx import Resource, Namespace, fields
from src.castingagency.api.models.movie import Movie, MovieSchema

movie_namespace = Namespace("Movies", description='Movies')

movie_model = movie_namespace.model(
    "Movie",
    {
        "title": fields.String(description='Actor Name', example="Jamaal"),
        "release_date": fields.Date(example="1998-04-04"),
    },
)


class MoviesList(Resource):

    @movie_namespace.doc(description='Hello World')
    def get(self):
        """Hello"""
        movies = MovieSchema().dump(Movie.query.all(), many=True)
        response_object = {
            'success': True,
            'movies': movies
        }
        return response_object, 200

    @movie_namespace.doc(description='Hello World')
    @movie_namespace.expect(movie_model)
    def post(self):
        "Hello"
        try:
            post_data = request.get_json()
            movie = MovieSchema().load(post_data)
            Movie(title=movie.title, release_date=movie.release_date).insert()
            response_object = {
                'success': True,
                'message': f'{movie.title} was added!'
            }
            return response_object, 201
        except:
            movie_namespace.abort(422, succcess=False, message="unprocessable")


class Movies(Resource):

    @movie_namespace.doc(description='Hello World')
    @movie_namespace.response(200, "<movie_id> was updated!")
    @movie_namespace.response(404, "Movie <movie_id> does not exist")
    @movie_namespace.response(422, "unprocessable")
    def get(self, movie_id):
        "Hello"
        movie = MovieSchema().dump(Movie.query.get(movie_id))
        if not movie:
            movie_namespace.abort(404, success=False,
                                  message=f"User {movie_id} does not exist")
        response_object = {
            'success': True,
            'movies': [movie]
        }
        return response_object, 200

    @movie_namespace.doc(description='Hello World')
    @movie_namespace.expect(movie_model)
    @movie_namespace.response(200, "<movie_id> was updated!")
    @movie_namespace.response(404, "Movie <movie_id> does not exist")
    @movie_namespace.response(422, "unprocessable")
    def patch(self, movie_id):
        "Hello"
        movie = Movie.query.get(movie_id)
        if not movie:
            movie_namespace.abort(404, f"User {movie_id} does not exist")
        try:
            body = request.get_json()
            movie = MovieSchema().load(body, instance=movie, partial=True)
            movie.update()
            response_object = {
                'success': True,
                'message': f'{movie.id} was updated!'
            }
            return response_object, 200
        except:
            movie_namespace.abort(422, succcess=False, message="unprocessable")

    @movie_namespace.doc(description='Hello World')
    @movie_namespace.response(200, "<movie_id> was removed!")
    @movie_namespace.response(404, "Movie <movie_id> does not exist")
    @movie_namespace.response(422, "unprocessable")
    def delete(self, movie_id):
        "Hello"
        movie = Movie.query.get(movie_id)
        if not movie:
            movie_namespace.abort(404, f"Movie {movie_id} does not exist")
        try:
            movie.delete()
            response_object = {
                'message': f'{movie.id} was deleted!'
            }
            return response_object, 200
        except:
            movie_namespace.abort(422, succcess=False, message="unprocessable")


movie_namespace.add_resource(MoviesList, '')
movie_namespace.add_resource(Movies, '/<int:movie_id>')
