from functools import wraps

from flask import jsonify, request, render_template

from src.validators.abstractions import BaseValidator


def validate_user_data(http_verb):
    def decorator_validate_user_data(func):
        @wraps(func)
        def wrapper_validate_user_data(*args, **kwargs):
            validation_error = UserValidator(request.form, http_verb).validate()
            if validation_error:
                return render_template('signup.html', error_message=validation_error)

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
                'error': f'missing required fields. Username: {username}, Password: {password}'}, 400

        error = self.validate_username(username)
        if error:
            return error

        error = self.validate_password(password)
        if error:
            return error

        return None

    def validate_update(self):
        username = self.data.get('username')
        password = self.data.get('password')

        if username is not None:
            error = self.validate_username(username)
            if error:
                return error

        if password is not None:
            error = self.validate_password(password)
            if error:
                return error

        return None
