import uuid
from datetime import datetime

from flask import Blueprint, jsonify, request, render_template, session
from flask_login import login_required

from src.apis.user_api import admin_permission
from src.models import Order, OrderState

order_api_blueprint = Blueprint('order_api_blueprint', __name__)


@order_api_blueprint.route('/orders', methods=['GET'])
@login_required
def get_order():
    order_id = session.get('order_id')
    if order_id:
        order = Order.query.get(order_id)
        if order:
            total_price = sum(item.price for item in order.order_items)
            return render_template('order.html', order=order, total_price=total_price)

    return render_template('order.html', order=None, total_price=0)


@order_api_blueprint.route('/orders/<id>', methods=['GET'])
# @login_required
# @admin_permission.require(http_exception=403)
def get_order_by_id(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(order.to_dict())


@order_api_blueprint.route('/orders', methods=['POST'])
@login_required
def create_order():
    order_items = request.form.getlist('order_item')
    if not order_items:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        order = Order.create(id=str(uuid.uuid4()), created_at=datetime.utcnow(), order_items=order_items)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify(order.to_dict()), 201


@order_api_blueprint.route('/orders/<id>', methods=['PUT'])
@admin_permission.require(http_exception=403)
@login_required
def update_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order_items = request.form.getlist('order_item')
    if not order_items:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        order.update(order_items)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify(order.to_dict())


@order_api_blueprint.route('/orders/<id>', methods=['PATCH'])
def update_order_state(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order_state = request.json.get('state')
    if not order_state:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        order.update_state(OrderState(order_state))
        return jsonify({'success': f'Order {id} state updated to {order_state}'}), 200
    except ValueError:
        return jsonify({'error': f'Invalid order state: {order_state}'}), 400


@order_api_blueprint.route('/orders/<id>', methods=['DELETE'])
@login_required
@admin_permission.require(http_exception=403)
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order.delete()
    return '', 204
