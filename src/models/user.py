from src import auth
from src import db


class User(db.Model):
    """
    Represents a user in the application.

    Attributes:
        id (int): A unique identifier for the user.
        username (str): The user's username.
        password (str): The user's password.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


@auth.verify_password
def verify_password(username, password):
    """
    Verify that the provided username and password are valid.

    Args:
        username (str): The username to verify.
        password (str): The password to verify.

    Returns:
        bool: True if the username and password are valid, False otherwise.
    """
    user = User.query.filter_by(username=username).first()
    if not user or not user.password == password:
        return False
    return user
