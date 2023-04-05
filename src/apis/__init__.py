# src/apis/__init__.py
from .redirect_api import redirect_api_blueprint
from .user_api import user_api_blueprint
from .order_api import order_api_blueprint
from .order_item_api import order_item_api_blueprint


def register_blueprints(app):
    app.register_blueprint(user_api_blueprint)
    app.register_blueprint(order_item_api_blueprint)
    app.register_blueprint(order_api_blueprint)
    app.register_blueprint(redirect_api_blueprint)
