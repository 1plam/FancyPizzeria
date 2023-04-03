from flask import Blueprint, jsonify, request
from flask_login import login_required

from src.models import OrderItem
from src.validators.order_item_validator import validate_order_item

order_item_api_blueprint = Blueprint('order_item_api_blueprint', __name__)


@order_item_api_blueprint.route('/order-items', methods=['GET'])
@login_required
def get_order_items():
    order_items = OrderItem.query.all()
    return jsonify([item.to_dict() for item in order_items])


@order_item_api_blueprint.route('/order-items/<id>', methods=['GET'])
@login_required
def get_order_item(id):
    order_item = OrderItem.query.get(id)
    if order_item is None:
        return jsonify({'error': 'OrderItem not found'}), 404

    return jsonify(order_item.to_dict())


@order_item_api_blueprint.route('/order-items', methods=['POST'])
@login_required
@validate_order_item
def create_order_item():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request data'}), 400

    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    if not all([name, price]):
        return jsonify({'error': 'Missing required fields'}), 400

    order_item = OrderItem.create(name=name, description=description, price=price)
    return jsonify(order_item.to_dict()), 201


@order_item_api_blueprint.route('/order-items/<id>', methods=['PUT'])
@login_required
@validate_order_item
def update_order_item(id):
    order_item = OrderItem.query.get(id)
    if order_item is None:
        return jsonify({'error': 'OrderItem not found'}), 404

    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request data'}), 400

    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    order_item.update(name=name, description=description, price=price)
    return jsonify(order_item.to_dict()), 200


@order_item_api_blueprint.route('/order-items/<id>', methods=['DELETE'])
@login_required
def delete_order_item(id):
    order_item = OrderItem.query.get(id)
    if order_item is None:
        return jsonify({'error': 'OrderItem not found'}), 404

    order_item.delete()
    return jsonify({'message': 'OrderItem deleted'}), 200
