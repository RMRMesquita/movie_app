from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import User, Movie, Rating

# User Registration Schema
class UserRegistrationSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

# User Login Schema
class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

# Movie Schema
class MovieSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        include_relationships = True
        load_instance = True

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    genre = fields.Str(required=True)
    duration = fields.Int(required=True)
    rating = fields.Float()
    director = fields.Str()
    producer = fields.Str()
    actors = fields.Str()

# Rating Schema
class RatingSchema(Schema):
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))

# Favorite Movies Schema
class FavoriteMoviesSchema(Schema):
    movie_id = fields.Int(required=True)

# Response schemas for user favorite movies list
class UserFavoriteMoviesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        load_instance = True

    id = fields.Int(dump_only=True)
    title = fields.Str()
    genre = fields.Str()
    duration = fields.Int()
    rating = fields.Float()
