import uuid

from src.context import db


class OrderItem(db.Model):
    """A class representing an order item."""
    __tablename__ = 'order_items'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float(precision=2), nullable=False)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=True)

    def to_dict(self):
        """Return a dictionary representation of the order item."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price
        }

    def __repr__(self):
        """Return a string representation of the order item."""
        return f'<OrderItem id={self.id} name={self.name} description={self.description} price={self.price} order_id={self.order_id}>'

    @classmethod
    def create(cls, name, description, price):
        """Create a new order item."""
        order_item = cls(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            price=price
        )
        db.session.add(order_item)
        db.session.commit()

        return order_item

    def update(self, name=None, description=None, price=None):
        """Update the order item."""
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if price is not None:
            self.price = price

        db.session.commit()

    def delete(self):
        """Delete the order item."""
        db.session.delete(self)
        db.session.commit()
