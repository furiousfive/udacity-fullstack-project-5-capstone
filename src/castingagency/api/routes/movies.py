from flask import Blueprint, request
from flask_restx import Resource, Api
from src.castingagency.api.models.movie import Movie, MovieSchema


movies_blueprint = Blueprint('movies', __name__)
api = Api(movies_blueprint)


class MoviesList(Resource):

    def get(self):
        movies = MovieSchema().dump(Movie.query.all(), many=True)
        response_object = {
            'success': True,
            'movies': movies
        }
        return response_object, 200

    def post(self):
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
            api.abort(422, succcess=False, message="unprocessable")


class Movies(Resource):

    def get(self, movie_id):
        movie = MovieSchema().dump(Movie.query.get(movie_id))
        if not movie:
            api.abort(404, success=False,  message=f"User {movie_id} does not exist")
        response_object = {
            'success': True,
            'movies': [movie]
        }
        return response_object, 200

    def patch(self, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            api.abort(404, f"User {movie_id} does not exist")
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
            api.abort(422, succcess=False, message="unprocessable")

    def delete(self, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            api.abort(404, f"Movie {movie_id} does not exist")
        try:
            movie.delete()
            response_object = {
                 'message': f'{movie.id} was deleted!'
            }
            return response_object, 200
        except:
            api.abort(422, succcess=False, message="unprocessable")


api.add_resource(MoviesList, '/movies')
api.add_resource(Movies, '/movies/<int:movie_id>')

