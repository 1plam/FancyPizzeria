import json

from oven.models import OrderState


class OrderStateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, OrderState):
            return str(obj)
        return OrderStateEncoder.default(self, obj)
