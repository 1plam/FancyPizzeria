from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required

from src.apis.user_api import admin_permission
from src.models import Order, OrderItem, OrderState


kitchen_api_blueprint = Blueprint('kitchen_api_blueprint', __name__)


@kitchen_api_blueprint.route('/kitchen', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_orders():
    orders = Order.query.all()
    order_list = []
    for order in orders:
        order_items = OrderItem.query.filter_by(order_id=order.id).all()
        item_list = []
        for item in order_items:
            item_list.append(item.to_dict())
        order_dict = order.to_dict()
        order_dict['order_items'] = item_list
        order_list.append(order_dict)
    return render_template('kitchen.html', orders=order_list, OrderState=OrderState)


@kitchen_api_blueprint.route('/kitchen/<id>', methods=['POST'])
@login_required
@admin_permission.require(http_exception=403)
def update_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    state = request.form.get('state')
    order.state = state

    order.save()
    return jsonify({'message': f'Order updated successfully'})
