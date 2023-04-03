import requests
from flask import request, jsonify
from flask_restful import Resource

from src import db, auth
from src.models.hackathon import Hackathon
from src.models.submission import Submission
from src.models.user import User


class sumbitHack(Resource):
    """
        A resource for submitting a hackathon project.
    """
    @auth.login_required
    def post(self):
        """
            Submit a new hackathon project.

            Args:
                None

            Returns:
                    A JSON response with a success message if the submission is successful,
                    or an error message if there is a validation error or the user/hackathon is not found.
        """
        data = request.get_json()
        # Extract submission data from the request
        name = data.get('name')
        summary = data.get('summary')
        submission_type = data.get('submission_type')
        submission_url = data.get('submission_url')
        username = auth.username()
        hackathon_id = data.get("hackathon_id")

        # Check if the user and hackathon exist
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'User not found'})
        print(hackathon_id)
        hackathon = Hackathon.query.filter_by(id=hackathon_id).first()
        if not hackathon:
            return jsonify({'message': 'Hackathon not found'})

        # Validate the submission URL based on its type
        if submission_type == 'image':
            if not is_image_url(submission_url):
                return jsonify({'message': 'Invalid image URL'})
        elif submission_type == 'file':
            if not is_file_url(submission_url):
                return jsonify({'message': 'Invalid file URL'})
        elif submission_type == 'link':
            if not is_valid_url(submission_url, submission_type):
                return jsonify({'message': 'Invalid link URL'})
        else:
            return jsonify({'message': 'Invalid submission type'})

        # Create a new submission object and add it to the database
        submission = Submission(name=name, summary=summary, submission_type=submission_type,
                                submission_url=submission_url,
                                user=user, hackathon=hackathon)
        db.session.add(submission)
        db.session.commit()

        response_data = {"message": "Submission received successfully"}
        response = jsonify(response_data)
        response.status_code = 200
        print("ok")
        return response


def is_image_url(url):
    """Check if a URL is a valid image URL"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
        content_type = response.headers.get('content-type')
        if content_type:
            return True
        else:
            return False
    except:
        return False


def is_file_url(url):
    """Check if a URL is a valid file URL"""
    try:
        response = requests.head(url)
        content_type = response.headers.get('content-type')
        if content_type:
            return True
        else:
            return False
    except:
        return False


def is_valid_url(url, submission_type):
    """Check if a URL is a valid submission URL based on submission type"""
    if submission_type == 'image':
        return is_image_url(url)
    elif submission_type == 'file':
        return is_file_url(url)
    elif submission_type == 'link':
        return True  # No validation needed for links
    else:
        return False  # Invalid submission type
