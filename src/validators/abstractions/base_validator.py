import re
from abc import ABC, abstractmethod


class BaseValidator(ABC):
    def __init__(self, data, method):
        self.data = data
        self.method = method
        self.validation_methods = {
            'POST': self.validate_create,
            'PUT': self.validate_update
        }

    def validate(self):
        validate_method = self.validation_methods.get(self.method)
        if validate_method:
            return validate_method()

        return {'error': 'Validation error: Invalid HTTP request method'}, 400

    @abstractmethod
    def validate_create(self):
        pass

    @abstractmethod
    def validate_update(self):
        pass

    @staticmethod
    def validate_username(username):
        if not username:
            error_message = 'username is required'
            return error_message

        if len(username) < 4 or len(username) > 12:
            error_message = 'username must be between 4 and 12 characters'
            return error_message

        return None

    @staticmethod
    def validate_password(password):
        if not password:
            error_message = 'password is required'
            return error_message

        if not re.match(r'^(?=[^a-z]*[a-z])(?=[^A-Z]*[A-Z])(?=\D*\d)(?=[^!#%]*[!#%])[A-Za-z0-9!#%]{6,32}$', password):
            error_message = 'password must contain at least one lowercase letter, one uppercase ' \
                            'letter, one digit, and one special character (!, #, or %) and be between 6 and 32 ' \
                            'characters'
            return error_message

        return None
