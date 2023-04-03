from src import db


class Registration(db.Model):
    """
      Represents a registration for a hackathon event.

      Attributes:
          id (int): A unique identifier for the registration.
          user_id (int): The ID of the user who registered.
          hackathon_id (int): The ID of the hackathon event the user registered for.
          user (relationship): The relationship between the Registration and User models.
          hackathon (relationship): The relationship between the Registration and Hackathon models.
      """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hackathon_id = db.Column(db.Integer, db.ForeignKey('hackathon.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('registrations', lazy=True))
    hackathon = db.relationship('Hackathon', backref=db.backref('registrations', lazy=True))

    def __repr__(self):
        """
               Returns a string representation of a registration object.

               Returns:
                   str: A string representation of a registration object.
        """
        return f'<Registration {self.id}>'
