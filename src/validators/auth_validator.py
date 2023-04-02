from flask import request, jsonify
from functools import wraps


class AuthValidator:
    @staticmethod
    def validate_login(data):
        username = data.get('username')
        password = data.get('password')

        if not all([username, password]):
            return {'error': 'Validation error: Missing required fields'}, 400

        return None, None


def validate_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Validation error: Invalid request data'}), 400

        validation_error, _ = AuthValidator.validate_login(data)
        if validation_error:
            return jsonify(validation_error), 400

        return func(*args, **kwargs)

    return wrapper
