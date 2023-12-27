"""Export class for Flask application configuration.

Supported by an .env file.
"""


import os
import redis

import dotenv

dotenv.load_dotenv()

POSTGRES_NAME = os.environ.get('POSTGRES_NAME')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')

REDIS_URL = os.environ.get('REDIS_URL')

class ApplicationConfig:
    """Flask application configuration."""

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/railway"

    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url(REDIS_URL)

    CORS_HEADERS = 'Content-Type'