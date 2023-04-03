from functools import wraps

from flask import jsonify, request

from src.validators.abstractions import BaseValidator


def validate_order_item(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        validator = OrderItemValidator(request.get_json(), request.method)
        validation_result, status_code = validator.validate()
        if validation_result:
            return jsonify(validation_result), status_code
        return view_func(*args, **kwargs)

    return wrapper

class OrderItemValidator(BaseValidator):
    def __init__(self, data, method):
        super().__init__(data, method)
        self.validation_methods = {
            'POST': self.validate_create,
            'PUT': self.validate_update
        }

    def validate_create(self):
        name = self.data.get('name')
        description = self.data.get('description')
        price = self.data.get('price')

        if not all([name, price]):
            return {'error': 'Validation error: Missing required fields'}, 400

        if not isinstance(name, str):
            return {'error': 'Validation error: Name must be a string'}, 400

        if description is not None and not isinstance(description, str):
            return {'error': 'Validation error: Description must be a string'}, 400

        if not isinstance(price, (int, float)) or price < 0:
            return {'error': 'Validation error: Price must be a non-negative number'}, 400

        return None, None

    def validate_update(self):
        name = self.data.get('name')
        description = self.data.get('description')
        price = self.data.get('price')

        if name is not None and not isinstance(name, str):
            return {'error': 'Validation error: Name must be a string'}, 400

        if description is not None and not isinstance(description, str):
            return {'error': 'Validation error: Description must be a string'}, 400

        if price is not None and (not isinstance(price, (int, float)) or price < 0):
            return {'error': 'Validation error: Price must be a non-negative number'}, 400

        return None, None
