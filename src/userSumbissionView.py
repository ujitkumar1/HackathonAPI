from flask import jsonify
from flask_restful import Resource

from src import auth
from src.models.hackathon import Hackathon
from src.models.submission import Submission
from src.models.user import User


class UserSumbission(Resource):
    """
        A Flask-RESTful resource representing all submissions made by a specific user for a specific hackathon.
    """
    @auth.login_required
    def get(self, user_id, hackathon_id):
        """
            Handles HTTP GET requests for the resource.

            Args:
                    user_id (int): The ID of the user whose submissions to retrieve.
                    hackathon_id (int): The ID of the hackathon for which to retrieve submissions.

            Returns:
                    A Flask response containing a JSON array of serialized submissions.
        """
        # Get the user and hackathon objects from the database
        user = User.query.get(user_id)
        hackathon = Hackathon.query.get(hackathon_id)

        # Check if the user and hackathon exist
        if not user or not hackathon:
            return jsonify({'message': 'User or hackathon not found'}), 404

        # Get all submissions for the user and hackathon
        submissions = Submission.query.filter_by(user_id=user_id, hackathon_id=hackathon_id).all()

        # Serialize the submissions and return as JSON response
        serialized_submissions = []
        for submission in submissions:
            serialized_submission = {
                'id': submission.id,
                'name': submission.name,
                'summary': submission.summary,
                'submission_type': submission.submission_type,
                'submission_url': submission.submission_url,
                'user_id': submission.user_id,
                'hackathon_id': submission.hackathon_id
            }
            serialized_submissions.append(serialized_submission)

        return jsonify(serialized_submissions)
