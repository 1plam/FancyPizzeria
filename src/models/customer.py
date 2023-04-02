import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from src.context import db


class Customer(UserMixin, db.Model):
    """A class representing a customer."""
    __tablename__ = 'customers'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    def to_dict(self):
        """Return a dictionary representation of the customer."""
        return {
            'id': repr(self.id),
            'username': self.username,
            'date_of_birth': self.date_of_birth.isoformat(),
        }

    def __repr__(self):
        """Return a string representation of the customer."""
        return f"<Customer id={self.id}, username='{self.username}', date_of_birth={self.date_of_birth}>"

    @staticmethod
    def hash_password(password):
        """Generate password hash from plain text password."""
        return generate_password_hash(password)

    def set_password(self, password):
        """Set the password hash for the customer."""
        self.password_hash = Customer.hash_password(password)

    def check_password(self, password):
        """Check if the given password is correct."""
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        """Return True if the customer is active."""
        return True

    def get_id(self):
        """Return the ID of the customer as a string."""
        return str(self.id)

    @classmethod
    def create(cls, username, password, date_of_birth):
        """Create a new customer."""
        customer = cls(
            id=str(uuid.uuid4()),
            username=username,
            date_of_birth=date_of_birth,
        )
        customer.set_password(password)
        db.session.add(customer)
        db.session.commit()

        return customer

    def update(self, username=None, password=None, date_of_birth=None):
        """Update an existing customer."""
        if username is not None:
            self.username = username
        if password is not None:
            self.set_password(password)
        if date_of_birth is not None:
            self.date_of_birth = date_of_birth

        db.session.commit()

    @classmethod
    def delete(cls, customer):
        """Delete an existing customer."""
        db.session.delete(customer)
        db.session.commit()
