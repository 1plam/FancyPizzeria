import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_principal import Principal

from src.apis import register_blueprints
from src.context import db
from src.handlers import login_manager, load_identity_when_session_exists, register_error_handlers

load_dotenv()

app = Flask(__name__, template_folder='templates', static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

login_manager.init_app(app)
principals = Principal(app)

load_identity_when_session_exists(app)

register_error_handlers(app)
register_blueprints(app)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
