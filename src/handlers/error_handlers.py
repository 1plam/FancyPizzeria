from flask import jsonify


def handle_forbidden_error(e):
    return jsonify(
        {'error': 'Forbidden', 'message': 'You do not have the required permissions to access this resource.'}), 403


def register_error_handlers(app):
    app.register_error_handler(403, handle_forbidden_error)
