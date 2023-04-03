from flask import request, jsonify, make_response
from flask_restful import Resource

from src import db, auth
from src.models.hackathon import Hackathon
from src.models.registration import Registration
from src.models.user import User


class RegesterHack(Resource):
    """
       Resource to handle registration of a user to a hackathon.
    """
    @auth.login_required
    def post(self):
        """
            POST method to register a user to a hackathon.

            Request body should contain:
                {
                    "user_id": <user_id>,
                    "hackathon_id": <hackathon_id>
                }

            Returns:
                - 200 if the registration was successful
                - 400 if the request body is missing a required field
                - 404 if either the user or the hackathon is not found
                """
        data = request.get_json()
        print(data.get('user_id'), data.get('hackathon_id'))
        # Extract user_id and hackathon_id from the request data
        user_id = data.get('user_id')
        hackathon_id = data.get('hackathon_id')

        # Check if the user and hackathon exist
        user = User.query.get(user_id)
        hackathon = Hackathon.query.get(hackathon_id)
        if not user or not hackathon:
            return jsonify({'message': 'User or hackathon not found'}), 404

        # Create a new registration object and add it to the database
        registration = Registration(user_id=user_id, hackathon_id=hackathon_id)

        db.session.add(registration)
        db.session.commit()

        # Return a success message
        response = make_response(jsonify({'message': 'Registration successful'}), 200)
        return response.get_json()
