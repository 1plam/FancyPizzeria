from flask_login import LoginManager
from src.models import User

login_manager = LoginManager()


@login_manager.unauthorized_handler
def unauthorized():
    return {"message": "You must be logged in to access this resource."}, 401


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
