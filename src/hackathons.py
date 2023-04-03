from dateutil import parser
from flask import request
from flask_restful import Resource

from src import db, auth
from src.models.hackathon import Hackathon


class Hackathons(Resource):
    """
    This module defines a Flask RESTful resource for handling HTTP requests related to Hackathon.
    The resource provides methods to create a new hackathon and get a list of all hackathons.

    Endpoints:

    POST /hackathons: Creates a new hackathon.
    GET /hackathons: Retrieves a list of all hackathons.
    Authentication:
    The POST method requires authentication using HTTP Basic Auth.

    Error codes:

    400 Bad Request: If the request is missing required fields.
    401 Unauthorized: If the user is not authenticated for the POST method.
    404 Not Found: If no hackathons are found.
    Classes:

    Hackathons(Resource): Flask RESTful resource for handling HTTP requests related to Hackathon.
    """
    @auth.login_required
    def post(self):
        title = request.json.get('title')
        description = request.json.get('description')
        background_image = request.json.get('background_image')
        hackathon_image = request.json.get('hackathon_image')
        submission_type = request.json.get('submission_type')
        start_datetime_str = request.json.get('start_datetime')
        end_datetime_str = request.json.get('end_datetime')
        reward_prize = request.json.get('reward_prize')
        user_id = auth.current_user().id

        if not all([title, description, start_datetime_str, end_datetime_str]):
            return {'error': 'Title, description, start_datetime, and end_datetime are required.'}, 400

        start_datetime = parser.isoparse(start_datetime_str).replace(tzinfo=None)
        end_datetime = parser.isoparse(end_datetime_str).replace(tzinfo=None)

        hackathon = Hackathon(title=title, description=description, background_image=background_image,
                              hackathon_image=hackathon_image,
                              submission_type=submission_type, start_datetime=start_datetime, end_datetime=end_datetime,
                              reward_prize=reward_prize, user_id=user_id)
        db.session.add(hackathon)
        db.session.commit()

        return {'message': 'Hackathon created successfully.'}, 201

    def get(self):
        hackathons = Hackathon.query.all()

        if not hackathons:
            return {'message': 'No hackathons found.'}, 404

        hackathon_list = []
        for hackathon in hackathons:
            hackathon_dict = {
                'id': hackathon.id,
                'title': hackathon.title,
                'description': hackathon.description,
                'background_image': hackathon.background_image,
                'hackathon_image': hackathon.hackathon_image,
                'submission_type': hackathon.submission_type,
                'start_datetime': hackathon.start_datetime.isoformat(),
                'end_datetime': hackathon.end_datetime.isoformat(),
                'reward_prize': hackathon.reward_prize,
                'user_id': hackathon.user_id
            }
            hackathon_list.append(hackathon_dict)

        return {'hackathons': hackathon_list}, 200
