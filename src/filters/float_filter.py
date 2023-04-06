def load_filters(app):
    @app.template_filter('floatformat')
    def float_format(value, digits=2):
        try:
            value = float(value)
            return f"{value:.{digits}f}"
        except (ValueError, TypeError):
            return value
