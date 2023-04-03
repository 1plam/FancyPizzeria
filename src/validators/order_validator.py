from functools import wraps

from flask import jsonify, request


def validate_order(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        validator = OrderValidator(request.get_json(), request.method)
        validation_result, status_code = validator.validate()
        if validation_result:
            return jsonify(validation_result), status_code
        return view_func(*args, **kwargs)
    return wrapper


class OrderValidator:
    def __init__(self, data, method):
        self.data = data
        self.method = method
        self.validation_methods = {

        }

    def validate(self):
        validate_method = self.validation_methods.get(self.method)
        if validate_method:
            return validate_method()

        return {'error': 'Validation error: Invalid HTTP request method'}, 400

