from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Store only hashed passwords
    role = db.Column(db.String(10), nullable=False, default='user')  # 'user' or 'admin'
    favorites = db.relationship('Movie', secondary='favorite_movies', lazy='subquery',
                                  backref=db.backref('favorited_by', lazy=True))

    def set_password(self, password):
        """Hash the password for storage."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password against the stored hash."""
        return check_password_hash(self.password_hash, password)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    actors = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(120), nullable=False)
    producer = db.Column(db.String(120), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # duration in minutes
    rating = db.Column(db.Float, nullable=False)
    genre = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        """Convert the Movie object to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'actors': self.actors,
            'director': self.director,
            'producer': self.producer,
            'duration': self.duration,
            'rating': self.rating,
            'genre': self.genre,
        }

class FavoriteMovies(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
