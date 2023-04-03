from src import db


class Submission(db.Model):
    """
    Represents a submission for a hackathon event.

    Attributes:
        id (int): A unique identifier for the submission.
        name (str): The name of the submission.
        summary (str): A summary of the submission.
        submission_type (str): The type of submission (image, file, or link).
        submission_url (str): The URL of the submission.
        user_id (int): The ID of the user who submitted the submission.
        user (relationship): The relationship between the Submission and User models.
        hackathon_id (int): The ID of the hackathon event the submission is for.
        hackathon (relationship): The relationship between the Submission and Hackathon models.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(500), nullable=False)
    submission_type = db.Column(db.Enum('image', 'file', 'link'), nullable=False)
    submission_url = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('submissions', lazy=True))
    hackathon_id = db.Column(db.Integer, db.ForeignKey('hackathon.id'), nullable=False)
    hackathon = db.relationship('Hackathon', backref=db.backref('submissions', lazy=True))
