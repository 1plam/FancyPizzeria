import uuid

from src.context import db
from .order_item import OrderItem


class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'order_items': [item.to_dict() for item in self.order_items]
        }

    def __repr__(self):
        return f'<Order id={self.id} created_at={self.created_at} order_items={self.order_items}>'

    @staticmethod
    def create(id, created_at, order_items):
        """Create a new order with the given items."""
        order = Order(id=id, created_at=created_at)

        for item_data in order_items:
            item_uuid = item_data['id']
            existing_item = OrderItem.query.filter_by(id=item_uuid).first()

            if not existing_item:
                raise ValueError(f"Item with ID {item_uuid} does not exist in the database.")

            order_item = OrderItem(id=uuid.uuid4(), name=existing_item.name, description=existing_item.description,
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

            order_item = OrderItem(id=uuid.uuid4(), name=existing_item.name, description=existing_item.description,
                                   price=existing_item.price)
            order_item.order = self
            self.order_items.append(order_item)

        db.session.commit()

    def delete(self):
        """Delete the order."""
        db.session.delete(self)
        db.session.commit()
