"""Export a class for Flask application configuration."""

import os


class ApplicationConfig:
    """Flask application configuration."""

    MONGO_URI = os.environ.get('MONO_URI')
