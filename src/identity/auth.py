from flask_login import LoginManager
from src import Customer

login_manager = LoginManager()


@login_manager.unauthorized_handler
def unauthorized():
    return {"message": "You must be logged in to access this resource."}, 401


@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(user_id)
