from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required

from src.models import User
from src.validators.auth_validator import validate_login
from src.validators.user_validator import validate_user_data

user_api_blueprint = Blueprint('user_api_blueprint', __name__)


@user_api_blueprint.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    user_dicts = [user.to_dict() for user in users]
    return jsonify(user_dicts)


@user_api_blueprint.route('/users/<user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())


@user_api_blueprint.route('/users', methods=['POST'])
@validate_user_data('POST')
def create_user():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request data'}), 400

    existing_user = User.query.filter_by(username=data.get('username')).first()
    if existing_user is not None:
        return jsonify({'error': 'Username already exists'}), 409

    user = User.create(data.get('username'), data.get('password'), data.get('date_of_birth'))
    return jsonify(user.to_dict()), 201


@user_api_blueprint.route('/users/<user_id>', methods=['PUT'])
@login_required
@validate_user_data('PUT')
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request data'}), 400

    user.update(data.get('username'), data.get('password'), data.get('date_of_birth'))
    return jsonify(user.to_dict()), 200


@user_api_blueprint.route('/users/<user_id>', methods=['DELETE'])
@login_required
def delete_user_handler(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    User.delete(user)
    return jsonify({'message': 'User deleted'}), 200


@user_api_blueprint.route('/login', methods=['POST'])
@validate_login
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401

    login_user(user)
    return jsonify(user.to_dict()), 200


@user_api_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200
