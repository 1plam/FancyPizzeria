import re
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
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
            return {'error': 'Validation error: Username is required'}, 400

        if len(username) < 4 or len(username) > 12:
            return {'error': 'Validation error: Username must be between 4 and 12 characters'}, 400

        return None, None

    @staticmethod
    def validate_password(password):
        if not password:
            return {'error': 'Validation error: Password is required'}, 400

        if not re.match(r'^(?=[^a-z]*[a-z])(?=[^A-Z]*[A-Z])(?=\D*\d)(?=[^!#%]*[!#%])[A-Za-z0-9!#%]{6,32}$', password):
            return {
                'error': 'Validation error: Password must contain at least one lowercase letter, one uppercase '
                         'letter, one digit, and one special character (!, #, or %) and be between 6 and 32 '
                         'characters'}, 400

        return None, None

    @staticmethod
    def validate_date_of_birth(date_of_birth):
        if not date_of_birth:
            return {'error': 'Validation error: Date of birth is required'}, 400

        try:
            dob = parse(date_of_birth)
            age = relativedelta(datetime.utcnow(), dob).years
            if age < 18:
                return {'error': 'Validation error: Customers must be at least 18 years old'}, 400
        except ValueError:
            return {'error': 'Validation error: Invalid date format. Please use ISO 8601 format (YYYY-MM-DD)'}, 400

        return None, None
