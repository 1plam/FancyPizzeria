from flask_login import current_user
from flask_principal import Identity, identity_changed, RoleNeed

from flask_login import LoginManager
from src.models import User

login_manager = LoginManager()


@login_manager.unauthorized_handler
def unauthorized():
    return {"message": "You must be logged in to access this resource."}, 401


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


def load_identity_when_session_exists(app):
    @app.before_request
    def before_request_callback():
        identity = Identity(current_user.get_id())
        if current_user.is_authenticated:
            if current_user.role == 'administrator':
                identity.provides.add(RoleNeed('administrator'))
        identity_changed.send(app, identity=identity)