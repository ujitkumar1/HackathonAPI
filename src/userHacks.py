from flask import jsonify
from flask_restful import Resource

from src import auth
from src.models.registration import Registration
from src.models.user import User


class userHack(Resource):
    """
        This class represents the RESTful API for retrieving the list of hackathons that a particular user has registered to.

        Attributes:
            None

        Methods:
            get(self, user_id): Retrieves the list of hackathons that the user has registered to.
    """
    @auth.login_required
    def get(self, user_id):
        """
            Retrieves the list of hackathons that the user has registered to.

            Args:
                    user_id (int): The ID of the user.

            Returns:
                    A JSON response containing the list of hackathons that the user has registered to.
        """
        # Get the user object from the database
        user = User.query.get(user_id)

        # Check if the user exists
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Get the list of hackathons the user is registered to
        registrations = Registration.query.filter_by(user=user).all()

        # Serialize the list of hackathons
        hackathons = []
        for registration in registrations:
            hackathon = registration.hackathon
            hackathon_data = {
                'id': hackathon.id,
                'title': hackathon.title,
                'description': hackathon.description,
                'background_image': hackathon.background_image,
                'hackathon_image': hackathon.hackathon_image,
                'submission_type': hackathon.submission_type,
                'start_datetime': hackathon.start_datetime.isoformat(),
                'end_datetime': hackathon.end_datetime.isoformat(),
                'reward_prize': hackathon.reward_prize
            }
            hackathons.append(hackathon_data)

        return jsonify({'hackathons': hackathons})
