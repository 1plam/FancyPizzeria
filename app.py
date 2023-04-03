import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from src.apis.customer_api import customer_api_blueprint
from src.apis.order_api import order_api_blueprint
from src.apis.order_item_api import order_item_api_blueprint
from src.context.association_context_table import db
from src.identity.auth import login_manager

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

login_manager.init_app(app)

app.register_blueprint(customer_api_blueprint)
app.register_blueprint(order_item_api_blueprint)
app.register_blueprint(order_api_blueprint)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

