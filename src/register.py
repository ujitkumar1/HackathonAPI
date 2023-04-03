from flask import request
from flask_restful import Resource

from src import db
from src.models.user import User


class register(Resource):
    """
       Resource for creating a new user account.
    """
    def post(self):
        """
            Create a new user account.

            Request Body:
                   - username (str): The username for the new user.
                   - password (str): The password for the new user.

            Returns:
                   - If successful, returns a JSON response with a "message" key and a HTTP status code of 201 (Created).
                   - If unsuccessful, returns a JSON response with an "error" key and a HTTP status code of 400 (Bad Request)
                     or 409 (Conflict).
        """
        print(request.json)
        username = request.json.get('username')
        password = request.json.get('password')
        if not username or not password:
            return {'error': 'Username and password are required.'}, 400
        if User.query.filter_by(username=username).first():
            return {'error': 'User already exists.'}, 409
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully.'}, 201
