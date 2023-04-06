from flask import Blueprint, jsonify, request
from flask_login import login_required

from src.apis.user_api import admin_permission
from src.models import OrderItem
from src.validators.order_item_validator import validate_order_item

order_item_api_blueprint = Blueprint('order_item_api', __name__)


@order_item_api_blueprint.route('/order-items', methods=['GET'])
def get_order_items():
    order_items = OrderItem.query.all()
    order_items_dict = [item.to_dict() for item in order_items]
    return jsonify(order_items_dict)


@order_item_api_blueprint.route('/order-items/<id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_order_item(id):
    order_item = OrderItem.query.filter_by(id=id).first()
    if not order_item:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(order_item.to_dict())


@order_item_api_blueprint.route('/order-items', methods=['POST'])
@login_required
@validate_order_item
def create_order_item():
    name = request.form.get('name')
    price = request.form.get('price')

    if not all([name, price]):
        return jsonify({'error': 'Missing required fields'}), 400

    order_item = OrderItem.create(name=name, description=request.form.get('description'), price=price)
    return jsonify(order_item.to_dict()), 201


@order_item_api_blueprint.route('/order-items/<id>', methods=['PUT'])
@login_required
@validate_order_item
def update_order_item(id):
    order_item = OrderItem.query.get(id)
    if not order_item:
        return jsonify({'error': 'OrderItem not found'}), 404

    name = request.form.get('name')
    price = request.form.get('price')

    if not all([name, price]):
        return jsonify({'error': 'Missing required fields'}), 400

    order_item.update(name=name, description=request.form.get('description'), price=price)
    return jsonify(order_item.to_dict()), 200


@order_item_api_blueprint.route('/order-items/<id>', methods=['DELETE'])
@login_required
@admin_permission.require(http_exception=403)
def delete_order_item(id):
    order_item = OrderItem.query.get(id)
    if not order_item:
        return jsonify({'error': 'OrderItem not found'}), 404

    order_item.delete()
    return jsonify({'message': 'OrderItem deleted'}), 200
