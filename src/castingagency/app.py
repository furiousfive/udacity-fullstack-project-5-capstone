# from flask import Flask, jsonify, request, abort
# from src.castingagency.models.model import setup_db, Actor, Movie
# from flask_cors import CORS
#
# app = Flask(__name__)
# setup_db(app)
# CORS(app)
#
#
# @app.route('/')
# def index():
#     """Handles GET requests for sample ping.
#     This is used to test whether the app is set up well.
#     returns:
#         - success message
#     """
#     return jsonify({
#         'message': 'Udacity capstone project.',
#         'success': True
#     })
#
# @app.route('/movies')
# # @requires_auth('read:movies')
# def get_all_movies():
#     try:
#         movies = Movie.query.all()
#         movies = [movie.format() for movie in movies]
#         return jsonify({
#             'success': True,
#             'movies': movies
#         })
#     except:
#         abort(422)
#
# @app.route('/movies/<int:movie_id>/')
# # @requires_auth('read:actors')
# def get_movie(movie_id):
#     try:
#         movie = Movie.query.get(movie_id)
#         return jsonify({
#             'success': True,
#             'title': movie.title,
#             'release_date': movie.release_date,
#         })
#     except:
#         abort(422)
#
# @app.route('/actors')
# # @requires_auth('read:actors')
# def get_all_actors():
#     try:
#         actors = Actor.query.all()
#         actors = [actor.format() for actor in actors]
#         return jsonify({
#             'success': True,
#             'actors': actors
#         })
#     except:
#         abort(422)
#
# @app.route('/actors/<int:actor_id>/')
# # @requires_auth('read:actors')
# def get_actor(actor_id):
#     try:
#         actor = Actor.query.get(actor_id)
#         return jsonify({
#             'success': True,
#             'name': actor.name,
#             'age': actor.age,
#             'gender': actor.gender
#         })
#     except:
#         abort(422)
#
# @app.route('/actors', methods=['POST'])
# # @requires_auth('write:actors')
# def add_actor():
#     name = request.get_json().get('name')
#     age = request.get_json().get('age')
#     gender = request.get_json().get('gender')
#     try:
#         data = name and age and gender
#         if not data:
#             abort(400)
#     except (TypeError, KeyError):
#         abort(400)
#
#     try:
#         Actor(name=name, age=age, gender=gender).insert()
#         return jsonify({
#             'success': True,
#             'actor': name
#         }), 201
#     except:
#         abort(422)
#
# @app.route('/actors/<int:actor_id>/', methods=['PATCH'])
# # @requires_auth('update:actors')
# def edit_actor(actor_id):
#
#actor = Actor.query.get(actor_id)
#     if not actor:
#         abort(404)
#     actor.name = request.get_json().get('name', actor.name)
#     actor.age = request.get_json().get('age', actor.age)
#     actor.gender = request.get_json().get('gender', actor.gender)
#     # update
#     actor.update()
#     return jsonify({
#         'success': True,
#         'actor': actor.format()
#     }), 200
#
#
# @app.route('/actors/<int:actor_id>/', methods=['DELETE'])
# def delete_actor(actor_id):
#     """
#     Delete a question using question id
#     :param question_id: Id of the question to be deleted
#     :return: Id of the question that has been deleted
#     """
#     try:
#         actor = Actor.query.get(actor_id)
#         actor.delete()
#         return jsonify({
#             'success': True,
#             'deleted': actor_id
#         })
#     except:
#         abort(422)
#
#
# # Error Handling
#
# @app.errorhandler(400)
# def bad_request(error):
#     return jsonify({
#         "success": False,
#         "error": 400,
#         "message": "bad request"
#     }), 400
#
#
# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({
#         "success": False,
#         "error": 404,
#         "message": "not found"
#     }), 404
#
#
# @app.errorhandler(409)
# def duplicate(error):
#     return jsonify({
#         "success": False,
#         "error": 409,
#         "message": "duplicate"
#     }), 409
#
#
# @app.errorhandler(422)
# def unprocessable(error):
#     return jsonify({
#         "success": False,
#         "error": 422,
#         "message": "unprocessable"
#     }), 422
#
#
# # def create_app(test_config=None):
# #   # create and configure the app
# #   app = Flask(__name__)
# #   CORS(app)
# #
# #   return app
# #
# # APP = create_app()
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)