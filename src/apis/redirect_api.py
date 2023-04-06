from flask import Blueprint, render_template

redirect_api_blueprint = Blueprint('redirect_api', __name__)

ROUTES = [
    ('index', 'index.html'),
    ('menu', 'menu.html'),
    ('orders', 'order.html'),
    ('signup', 'signup.html'),
    ('login', 'login.html'),
    ('logout', 'index.html'),
    ('payment', 'payment.html'),
    ('kitchen', 'kitchen.html'),
]


@redirect_api_blueprint.route('/')
def handle_index():
    return render_template('index.html')


@redirect_api_blueprint.route('/<path:route>')
def handle_route(route):
    for r, template in ROUTES:
        if route == r:
            return render_template(template)
    return 'Not found', 404
