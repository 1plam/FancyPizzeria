import uuid

from src.context import db
from .order_item import OrderItem
from .order_state import OrderState


class Order(db.Model):
    """A class representing an order."""
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    state = db.Column(db.Enum(OrderState), default=OrderState.SUBMITTED)
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Return a dictionary representation of the order."""
        return {
            'id': self.id,
            'created_at': self.created_at,
            'state': self.state,
            'order_items': [item.to_dict() for item in self.order_items]
        }

    def __repr__(self):
        """Return a string representation of the order."""
        return f'<Order id={self.id} created_at={self.created_at} state={self.state} order_items={self.order_items}>'

    @staticmethod
    def create(id, created_at, order_items, state=OrderState.SUBMITTED):
        """Create a new order with the given items."""
        order = Order(id=id, created_at=created_at, state=state)

        for item in order_items:
            item_name = item['name']
            existing_item = OrderItem.query.filter_by(name=item_name).first()

            if not existing_item:
                raise ValueError(f"Item with name {item_name} does not exist in the database.")

            order_item = OrderItem(id=str(uuid.uuid4()), name=existing_item.name, description=existing_item.description,
                                   price=existing_item.price)
            order_item.order = order
            order.order_items.append(order_item)

        db.session.add(order)
        db.session.commit()

        return order

    def update(self, order_items):
        """Update the order items."""
        for order_item in self.order_items:
            db.session.delete(order_item)

        for item_data in order_items:
            item_uuid = item_data['id']
            existing_item = OrderItem.query.filter_by(id=item_uuid).first()

            if not existing_item:
                raise ValueError(f"Item with ID {item_uuid} does not exist in the database.")

            order_item = OrderItem(id=str(uuid.uuid4()), name=existing_item.name, description=existing_item.description,
                                   price=existing_item.price)
            order_item.order = self
            self.order_items.append(order_item)

        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the order."""
        db.session.delete(self)
        db.session.commit()
