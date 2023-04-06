from flask import Blueprint, jsonify, request, session, redirect, flash, render_template
from flask_login import login_user, logout_user, login_required
from flask_principal import Permission, RoleNeed

from src.models import User
from src.validators.auth_validator import validate_login
from src.validators.user_validator import validate_user_data

user_api_blueprint = Blueprint('user_api_blueprint', __name__)

admin_permission = Permission(RoleNeed('administrator'))


@user_api_blueprint.route('/users', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_users():
    users = User.query.all()
    user_dicts = [user.to_dict() for user in users]
    return jsonify(user_dicts), 200


@user_api_blueprint.route('/users/<id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


@user_api_blueprint.route('/users', methods=['POST'])
@validate_user_data('POST')
def create_user():
    username = request.form['username']
    password = request.form['password']

    if not [username, password]:
        error_message = 'invalid request data'
        return render_template('signup.html', error_message=error_message)

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        error_message = 'username already exists'
        return render_template('signup.html', error_message=error_message)

    user = User.create(username, password)
    return jsonify(user.to_dict()), 201


@user_api_blueprint.route('/users/<id>', methods=['PUT'])
@login_required
@validate_user_data('PUT')
def update_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    username = request.form.get('username')
    password = request.form.get('password')

    if not [username, password]:
        return jsonify({'error': 'Invalid request data'}), 400

    user.update(username, password)
    return jsonify(user.to_dict()), 200


@user_api_blueprint.route('/users/<id>', methods=['DELETE'])
@login_required
@admin_permission.require(http_exception=403)
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    User.delete(user)
    return jsonify({'message': 'User deleted'}), 200


@user_api_blueprint.route('/login', methods=['POST'])
@validate_login
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        error_message = 'invalid credentials. please check your login details and try again.'
        return render_template('login.html', error_message=error_message)

    login_user(user)

    if user.role == 'administrator':
        session['admin'] = True
        return redirect('/kitchen')

    return redirect('/index')


@user_api_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    if 'admin' in session:
        session.pop('admin')

    logout_user()
    return redirect("/index")
