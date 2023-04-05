from functools import wraps

from flask import jsonify, request

from src.validators.abstractions import BaseValidator


def validate_user_data(http_verb):
    def decorator_validate_user_data(func):
        @wraps(func)
        def wrapper_validate_user_data(*args, **kwargs):
            validation_error, _ = UserValidator(request.form, http_verb).validate()
            if validation_error:
                return jsonify(validation_error), 400

            return func(*args, **kwargs)

        return wrapper_validate_user_data

    return decorator_validate_user_data


class UserValidator(BaseValidator):
    def __init__(self, data, method):
        super().__init__(data, method)

    def validate_create(self):
        username = self.data.get('username')
        password = self.data.get('password')

        if not all([username, password]):
            return {
                'error': f'Missing required fields. Username: {username}, Password: {password}'}, 400

        error, status_code = self.validate_username(username)
        if error:
            return error, status_code

        error, status_code = self.validate_password(password)
        if error:
            return error, status_code

        return None, None

    def validate_update(self):
        username = self.data.get('username')
        password = self.data.get('password')
        date_of_birth = self.data.get('date_of_birth')

        if username is not None:
            error, status_code = self.validate_username(username)
            if error:
                return error, status_code

        if password is not None:
            error, status_code = self.validate_password(password)
            if error:
                return error, status_code

        return None, None
