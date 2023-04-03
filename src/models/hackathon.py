from src import db


class Hackathon(db.Model):
    """
       Represents a hackathon event.

       Attributes:
           id (int): A unique identifier for the hackathon event.
           title (str): The title of the hackathon event.
           description (str): A brief description of the hackathon event.
           background_image (str): The background image for the hackathon event.
           hackathon_image (str): The image representing the hackathon event.
           submission_type (Enum): The type of submission required for the hackathon event. Can be one of 'image', 'file', or 'link'.
           start_datetime (datetime): The start date and time of the hackathon event.
           end_datetime (datetime): The end date and time of the hackathon event.
           reward_prize (float): The prize amount for the hackathon event.
           user_id (int): The ID of the user who created the hackathon event.
           user (relationship): The relationship between the Hackathon and User models.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    background_image = db.Column(db.String(100), nullable=False)
    hackathon_image = db.Column(db.String(100), nullable=False)
    submission_type = db.Column(db.Enum('image', 'file', 'link'), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    reward_prize = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('hackathons', lazy=True))
