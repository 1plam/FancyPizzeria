import re
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from functools import wraps

from flask import jsonify


class CustomerValidator:
    def __init__(self, data, method):
        self.data = data
        self.method = method
        self.validation_methods = {
            'POST': self.validate_create_customer,
            'PUT': self.validate_update_customer,
            'DELETE': self.validate_delete_customer
        }

    def validate(self):
        validate_method = self.validation_methods.get(self.method)
        if validate_method:
            return validate_method()

        return {'error': 'Validation error: Invalid HTTP request method'}, 400

    def validate_create_customer(self):
        username = self.data.get('username')
        password = self.data.get('password')
        date_of_birth = self.data.get('date_of_birth')

        if not all([username, password, date_of_birth]):
            return {'error': 'Validation error: Missing required fields'}, 400

        if len(username) < 4 or len(username) > 12:
            return {'error': 'Validation error: Username must be between 4 and 12 characters'}, 400

        if not re.match(r'^(?=[^a-z]*[a-z])(?=[^A-Z]*[A-Z])(?=\D*\d)(?=[^!#%]*[!#%])[A-Za-z0-9!#%]{6,32}$', password):
            return {'error': 'Validation error: Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character (!, #, or %) and be between 6 and 32 characters'}, 400

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

    def validate_update_customer(self):
        username = self.data.get('username')
        password = self.data.get('password')
        date_of_birth = self.data.get('date_of_birth')

        if username is not None:
            if len(username) == 0:
                return {'error': 'Validation error: Username cannot be empty'}, 400
            elif len(username) < 4 or len(username) > 12:
                return {'error': 'Validation error: Username must be between 4 and 12 characters'}, 400

        if password is not None:
            if not re.match(r'^(?=[^a-z]*[a-z])(?=[^A-Z]*[A-Z])(?=\D*\d)(?=[^!#%]*[!#%])[A-Za-z0-9!#%]{6,32}$', password):
                return {'error': 'Validation error: Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character (!, #, or %) and be between 6 and 32 characters'}, 400

        try:
            dob = parse(date_of_birth)
            age = relativedelta(datetime.utcnow(), dob).years
            if age < 18:
                return {'error': 'Validation error: Customers must be at least 18 years old'}, 400
        except ValueError:
            return {'error': 'Validation error: Invalid date format. Please use ISO 8601 format (YYYY-MM-DD)'}, 400

        return None, None

    def validate_delete_customer(self):
        customer_id = self.data.get('customer_id')

        if not customer_id.isdigit():
            return {'error': 'Validation error: Invalid customer ID'}, 400

        return None, None


def validate_create_customer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = kwargs.get('data')
        validation_error, _ = CustomerValidator(data, 'POST').validate()
        if validation_error:
            return jsonify(validation_error), 400

        return func(*args, **kwargs)

    return wrapper


def validate_update_customer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        customer = kwargs.get('customer')
        data = kwargs.get('data')
        validation_error, _ = CustomerValidator(data, 'PUT').validate()
        if validation_error:
            return jsonify(validation_error), 400

        return func(*args, **kwargs)

    return wrapper


def validate_delete_customer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = kwargs.get('data')
        validation_error, _ = CustomerValidator(data, 'DELETE').validate()
        if validation_error:
            return jsonify(validation_error), 400

        return func(*args, **kwargs)

    return wrapper
