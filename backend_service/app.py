"""Define the service API endpoints and run the application.

This module defines the endpoints for the service and runs the server. This service is designed to handle traffic from
the client.

Endpoints:
    /auth/login: Login a user and start a server side session.
    /auth/register: Register a new user with the system.
"""

import flask
from flask import jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session

from config import ApplicationConfig
from models import db, User

app = flask.Flask(__name__)
app.config.from_object(ApplicationConfig)
bcrypt = Bcrypt(app)
db.init_app(app)
cors = CORS(app, supports_credentials=True)
with app.app_context():
    db.create_all()

server_session = Session(app)


@app.route('/auth/register', methods=['POST'])
def register_user():
    """Register new users.

    Payload:
        ```json
            {
                "email": "test@email.com",
                "password": "password"
            }
        ```
    """
    email = flask.request.json['email']
    password = flask.request.json['password']

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({'error': 'User already exists.'}), 409

    new_user = User(
        email=email,
        password=bcrypt.generate_password_hash(password).decode('utf-8')
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'id': new_user.id,
        'email': new_user.email
    })


@app.route('/auth/login', methods=['POST'])
def login_user():
    """Login a registered user."""
    email = flask.request.json['email']
    password = flask.request.json['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'No user with that email is registered.'}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Incorrect password.'}), 401

    session['user_id'] = user.id

    response = jsonify({
        'id': user.id,
        'email': user.email
    })

    return response


if __name__ == '__main__':
    app.run(debug=True)
