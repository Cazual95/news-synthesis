"""Export a class for Flask application configuration."""

import os

from dotenv import load_dotenv

load_dotenv()

MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = os.environ.get('MONGO_PORT')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME')
MONGO_AUTH_SOURCE = os.environ.get('MONGO_AUTH_SOURCE')


class ApplicationConfig:
    """Flask application configuration."""

    MONGO_URI = f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}?authSource={MONGO_AUTH_SOURCE}'
