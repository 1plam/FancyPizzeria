from datetime import datetime
from uuid import uuid4

from flask import Blueprint, jsonify, request, session, redirect, render_template
from flask_login import login_required

from src.models import Order

cart_api_blueprint = Blueprint('cart_api_blueprint', __name__)

CART_ITEMS_KEY = 'cart_items'


@cart_api_blueprint.route('/cart', methods=['GET'])
@login_required
def get_cart_items():
    cart_items = session.get(CART_ITEMS_KEY, [])
    return jsonify(cart_items)


@cart_api_blueprint.route('/cart', methods=['POST'])
@login_required
def add_to_cart():
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')

    if not all([name, description, price]):
        return jsonify({'error': 'Missing required fields'}), 400

    item = {'name': name, 'description': description, 'price': float(price)}
    cart_items = session.get(CART_ITEMS_KEY, [])
    cart_items.append(item)
    session[CART_ITEMS_KEY] = cart_items

    message = "Item was successfully added to cart"
    return render_template('menu.html', message=message)


@cart_api_blueprint.route('/cart/<item_name>', methods=['DELETE'])
@login_required
def remove_item_from_cart(item_name):
    item_name = item_name.replace('-', ' ')
    cart_items = session.get(CART_ITEMS_KEY, [])
    for i, item in enumerate(cart_items):
        if item['name'] == item_name:
            del cart_items[i]
            session[CART_ITEMS_KEY] = cart_items
            return redirect('/payment')
    return jsonify({'error': 'Item not found'}), 404


@cart_api_blueprint.route('/cart/checkout', methods=['POST'])
@login_required
def checkout():
    order_id = str(uuid4())
    order_items = session.get(CART_ITEMS_KEY, [])

    try:
        order_item_dicts = [{'name': item['name'], 'description': item['description'], 'price': item['price']}
                            for item in order_items]
        order = Order.create(id=order_id, created_at=datetime.utcnow(), order_items=order_item_dicts)
        session['order_id'] = order.id
        session.pop(CART_ITEMS_KEY, None)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return redirect("/orders")
