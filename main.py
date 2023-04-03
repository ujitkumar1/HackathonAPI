# Import necessary libraries and modules
from src import app, api
from src import db
from src.hackathons import Hackathons
from src.myHacathons import myHacathons
from src.register import register
from src.registerHack import RegesterHack
from src.sumbitHack import sumbitHack
from src.userHacks import userHack
from src.userSumbissionView import UserSumbission

# Add resource endpoints
api.add_resource(register, "/register")
api.add_resource(Hackathons, "/hackathons")
api.add_resource(myHacathons, "/my-hackathons")
api.add_resource(RegesterHack, "/register-hackathon")
api.add_resource(sumbitHack, "/submit-hackathon")
api.add_resource(userHack, "/my-hackathons/<int:user_id>")
api.add_resource(UserSumbission, "/my-submissions/<int:user_id>/<int:hackathon_id>")

# Create database tables and start the application
if __name__ == "__main__":
    db.create_all() # Create database tables
    app.run(
        debug=True,
        port=5000
    )
