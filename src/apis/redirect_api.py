from flask import Blueprint, render_template

redirect_api_blueprint = Blueprint('redirect_api', __name__)


@redirect_api_blueprint.route('/')
def index():
    return render_template('index.html')

@redirect_api_blueprint.route('/menu')
def menu():
    return render_template('menu.html')

@redirect_api_blueprint.route('/order')
def order():
    return render_template('order.html')

@redirect_api_blueprint.route('/login')
def login():
    return render_template('login.html')

@redirect_api_blueprint.route('/payment')
def payment():
    return render_template('payment.html')