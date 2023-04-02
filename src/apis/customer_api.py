from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required

from src.models import Customer
from src.validators import CustomerValidator, AuthValidator

customer_api_blueprint = Blueprint('customer_api_blueprint', __name__)


@customer_api_blueprint.route('/customers', methods=['GET'])
@login_required
def get_customers():
    customers = Customer.query.all()
    customer_dicts = [customer.to_dict() for customer in customers]
    return jsonify(customer_dicts)


@customer_api_blueprint.route('/customers/<customer_id>', methods=['GET'])
@login_required
def get_customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    if customer is None:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify(customer.to_dict())


@customer_api_blueprint.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request data'}), 400

    validator = CustomerValidator(data, request.method)
    error, status_code = validator.validate()
    if error:
        return jsonify(error), status_code

    existing_customer = Customer.query.filter_by(username=data.get('username')).first()
    if existing_customer is not None:
        return jsonify({'error': 'Username already exists'}), 409

    customer = Customer.create(data.get('username'), data.get('password'), data.get('date_of_birth'))
    return jsonify(customer.to_dict()), 201


@customer_api_blueprint.route('/customers/<customer_id>', methods=['PUT'])
@login_required
def update_customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    if customer is None:
        return jsonify({'error': 'Customer not found'}), 404

    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request data'}), 400

    validator = CustomerValidator(data, request.method)
    error, status_code = validator.validate()
    if error:
        return jsonify(error), status_code

    customer.update(data.get('username'), data.get('password'), data.get('date_of_birth'))
    return jsonify(customer.to_dict()), 200


@customer_api_blueprint.route('/customers/<customer_id>', methods=['DELETE'])
@login_required
def delete_customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    if customer is None:
        return jsonify({'error': 'Customer not found'}), 404

    Customer.delete(customer)
    return jsonify({'message': 'Customer deleted'}), 200


@customer_api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request data'}), 400

    validation_error, status_code = AuthValidator.validate_login(data)
    if validation_error:
        return jsonify(validation_error), status_code

    username = data.get('username')
    password = data.get('password')

    customer = Customer.query.filter_by(username=username).first()
    if customer is None or not customer.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401

    login_user(customer)
    return jsonify(customer.to_dict()), 200


@customer_api_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200
