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
        data = request.form
        validation_error, status_code = AuthValidator.validate_login(data)

        if validation_error:
            return jsonify(validation_error), status_code

        return func(*args, **kwargs)

    return wrapper
