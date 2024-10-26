from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, User, Movie, FavoriteMovies  # Import models

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)  # Initialize db with the app
jwt = JWTManager(app)

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'msg': 'Missing username, email or password!'}), 400

    new_user = User(
        username=data['username'],
        email=data['email'],
        role='user'  # Default role is 'user' for new registrations
    )
    new_user.set_password(data['password'])  # Hash the password using the model method

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': 'User created successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):  # Use model method to check password
        return jsonify({'msg': 'Bad username or password!'}), 401

    access_token = create_access_token(identity={'id': user.id, 'role': user.role})
    return jsonify(access_token=access_token), 200

@app.route('/movies', methods=['GET'])
@jwt_required()
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.to_dict() for movie in movies]), 200

@app.route('/movies', methods=['POST'])
@jwt_required()
def create_movie():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'msg': 'Access forbidden: Admins only!'}), 403

    data = request.get_json()
    new_movie = Movie(
        title=data['title'],
        actors=data['actors'],
        director=data['director'],
        producer=data['producer'],
        duration=data['duration'],
        rating=data['rating'],
        genre=data['genre']
    )
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({'msg': 'Movie created successfully!'}), 201

@app.route('/movies/<int:movie_id>', methods=['GET'])
@jwt_required()
def get_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return jsonify(movie.to_dict()), 200

@app.route('/movies/<int:movie_id>', methods=['PUT'])
@jwt_required()
def update_movie(movie_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'msg': 'Access forbidden: Admins only!'}), 403

    data = request.get_json()
    movie = Movie.query.get_or_404(movie_id)
    movie.title = data.get('title', movie.title)
    movie.actors = data.get('actors', movie.actors)
    movie.director = data.get('director', movie.director)
    movie.producer = data.get('producer', movie.producer)
    movie.duration = data.get('duration', movie.duration)
    movie.rating = data.get('rating', movie.rating)
    movie.genre = data.get('genre', movie.genre)

    db.session.commit()
    return jsonify({'msg': 'Movie updated successfully!'}), 200

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@jwt_required()
def delete_movie(movie_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'msg': 'Access forbidden: Admins only!'}), 403

    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()

    return jsonify({'msg': 'Movie deleted successfully!'}), 200

@app.route('/users/<int:user_id>/favorites', methods=['POST'])
@jwt_required()
def add_favorite(user_id):
    current_user = get_jwt_identity()
    if current_user['id'] != user_id:
        return jsonify({'msg': 'Access forbidden: You can only modify your own favorites!'}), 403

    data = request.get_json()
    movie = Movie.query.get_or_404(data['movie_id'])

    favorite = FavoriteMovies(user_id=user_id, movie_id=movie.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({'msg': 'Movie added to favorites!'}), 201

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
@jwt_required()
def get_favorites(user_id):
    current_user = get_jwt_identity()
    if current_user['id'] != user_id:
        return jsonify({'msg': 'Access forbidden: You can only view your own favorites!'}), 403

    favorites = FavoriteMovies.query.filter_by(user_id=user_id).all()
    favorite_movies = [Movie.query.get(favorite.movie_id).to_dict() for favorite in favorites]
    return jsonify(favorite_movies), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
