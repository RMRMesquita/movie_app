import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'  # Default for local development
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'default_jwt_secret_key'  # Default for local development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/db_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
