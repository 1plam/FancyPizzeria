import os
from datetime import datetime

import uuid
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from src.apis.user_api import user_api_blueprint
from src.apis.order_api import order_api_blueprint
from src.apis.order_item_api import order_item_api_blueprint
from src.context.association_context_table import db
from src.identity.auth import login_manager
from src.models import Order, OrderItem

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

login_manager.init_app(app)

app.register_blueprint(user_api_blueprint)
app.register_blueprint(order_item_api_blueprint)
app.register_blueprint(order_api_blueprint)

with app.app_context():
    db.create_all()

with app.app_context():
    order = Order(created_at=datetime.utcnow())

    order_item_1 = OrderItem(id=uuid.uuid4(), name='Hawaiian Pizza', description='Pineapple and ham pizza', price=12.99, order=order)
    order_item_2 = OrderItem(id=uuid.uuid4(), name='Fanta', description='Orange Fanta', price=1.99, order=order)
    order.order_items.append(order_item_1)
    order.order_items.append(order_item_2)

    db.session.add(order)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)

