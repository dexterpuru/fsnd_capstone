import os
import json
from flask import Flask, request, abort, jsonify
from sqlalchemy import exc
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db, setup_db, Actor, Movie, helper_table


def create_app(test_config=None):
    # Create and configure app
    # os.environ("SQLALCHEMY_DATABASE_URI") = "postgresql://postgres:puru2000@localhost/casting_agency"
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    migrate = Migrate(app, db)

    @app.route('/')
    def index():
        return "This is demo page of Casting Agency Api."

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PUT, POST, DELETE, OPTIONS'
        )
        return response

    # Actor Routes

    @app.route('/actors', methods=['GET'])
    @requires_auth('view:actors')
    def get_actors():
        try:
            actors = [actor.info() 
                    for actor in Actor.query.order_by(Actor.id).all()]

            return jsonify({
                'success': True,
                'status_code': 200,
                'status_message': 'OK',
                'actors': actors
            })
        except Exception as e:
            print(e)
            abort(422)


    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actors')
    def post_actors():
        name = request.json.get("name", None)
        age = request.json.get("age", None)
        gender = request.json.get("gender", None)
        seen_in_movies = request.json.get("movies", None)

        new_actor = Actor(name=name, age=age, gender=gender)

        for movie in seen_in_movies:
            new_actor.movies.append(Movie.query.get(movie))

        new_actor.insert()

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": "OK",
            "actor": new_actor.info()
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('edit:actors')
    def patch_actors(actor_id):
        name = request.json.get("name", None)
        age = request.json.get("age", None)
        gender = request.json.get("gender", None)
        seen_in_movies = request.json.get("movies", None)

        target_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if target_actor is None:
            abort(404)


        if seen_in_movies:
            target_actor.movies = []
            target_actor.update()

            for movie in seen_in_movies:
                target_actor.movies.append(Movie.query.get(movie))

        if name: target_actor.name = name
        if age: target_actor.age = age
        if gender: target_actor.gender = gender
        target_actor.update()

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "actor": target_actor.info()
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actors(actor_id):
        target_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if target_actor is None:
            abort(404)
        target_actor.delete()

        return jsonify({"success": True,
                        "status_code": 200,
                        "status_message": 'OK',
                        "id_deleted": actor_id})
        
    # Movie Routes

    @app.route('/movies', methods=["GET"])
    @requires_auth('view:movies')
    def get_movies():
        try:
            movies = [movie.info()
                    for movie in Movie.query.order_by(Movie.id).all()]
            return jsonify({
                "success": True,
                "status_code": 200,
                "status_message": 'OK',
                "movies": movies
            })
        except Exception:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='add:movies')
    def post_movies():
        title = request.json.get("title", None)
        release_date = request.json.get("release_date", None)
        actors = request.json.get('actors', None)

        if title is None:
            abort(422)

        new_movie = Movie(title=title, release_date=release_date)
            
        for i in actors:
            new_movie.actors.append(Actor.query.get(i))

        new_movie.insert()

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "movie": new_movie.info()
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth(permission='edit:movies')
    def patch_movies(movie_id):
        title = request.json.get("title", None)
        release_date = request.json.get("release_date", None)
        cast = request.json.get("cast", None)

        target_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if target_movie is None:
            abort(404)

        if cast:
            target_movie.actors = []
            target_movie.update()
            for person in cast:
                target_movie.actors.append(Actor.query.get(person))

        if title: target_movie.title = title
        if release_date: target_movie.release_date = release_date
        target_movie.update()

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "movie": target_movie.info()
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movies(movie_id):
        target_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if target_movie is None:
            abort(404)
        target_movie.delete()

        return jsonify({"success": True,
                        "status_code": 200,
                        "status_message": 'OK',
                        "id_deleted": movie_id})

    # Error Handeling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "status_message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "status_message": "resource Not found"
        }), 404

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify(error.error), error.status_code

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)