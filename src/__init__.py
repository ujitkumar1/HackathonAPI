import os

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# Create the Flask application instance
app = Flask(__name__)

# Create an instance of the HTTPBasicAuth class for user authentication
auth = HTTPBasicAuth()

# Set up the database connection and ORM
# Define the database URI based on the location of the database file
# Create an instance of the SQLAlchemy class to use for ORM
app.secret_key = "ujit1"
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'hackathons.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

# Create an instance of the Flask-RESTful API class
api = Api(app)
