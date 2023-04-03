from flask import jsonify
from flask_restful import Resource

from src import auth
from src.models.hackathon import Hackathon
from src.models.registration import Registration
from src.models.user import User


class myHacathons(Resource):
    """
       Resource for retrieving all hackathons that the currently authenticated user is enrolled in.
    """
    @auth.login_required
    def get(self):
        """
                Retrieves all hackathons that the currently authenticated user is enrolled in.

                Returns:
                    A JSON object containing a list of hackathons in which the user is enrolled.
                    Each hackathon is represented as a dictionary with the following keys:
                    - id: the hackathon's ID
                    - title: the hackathon's title
                    - description: the hackathon's description
                    - background_image: the URL of the hackathon's background image
                    - hackathon_image: the URL of the hackathon's image
                    - submission_type: the hackathon's submission type
                    - start_datetime: the hackathon's start datetime in ISO format
                    - end_datetime: the hackathon's end datetime in ISO format
                    - reward_prize: the hackathon's reward prize
                    - user_id: the ID of the user who created the hackathon
        """
        # Get the currently authenticated user
        user = User.query.filter_by(username=auth.username()).first()

        # Get a list of all the hackathons the user is enrolled in
        registrations = Registration.query.filter_by(user=user).all()
        hackathon_ids = [r.hackathon_id for r in registrations]
        hackathons = Hackathon.query.filter(Hackathon.id.in_(hackathon_ids)).all()

        # Manually serialize the hackathon data into a list of dictionaries
        hackathon_list = []
        for h in hackathons:
            hackathon_dict = {
                'id': h.id,
                'title': h.title,
                'description': h.description,
                'background_image': h.background_image,
                'hackathon_image': h.hackathon_image,
                'submission_type': h.submission_type,
                'start_datetime': h.start_datetime.isoformat(),
                'end_datetime': h.end_datetime.isoformat(),
                'reward_prize': h.reward_prize,
                'user_id': h.user_id
            }
            hackathon_list.append(hackathon_dict)

        # Return the serialized hackathon data as a JSON response
        return jsonify({'hackathons': hackathon_list})
