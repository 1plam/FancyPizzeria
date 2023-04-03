import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from src.context import db


class User(UserMixin, db.Model):
    """A class representing a user."""
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    user_id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    def to_dict(self):
        """Return a dictionary representation of the user."""
        return {
            'user_id': repr(self.user_id),
            'username': self.username,
            'date_of_birth': self.date_of_birth.isoformat(),
        }

    def __repr__(self):
        """Return a string representation of the user."""
        return f"<User user_id={self.user_id}, username='{self.username}', date_of_birth={self.date_of_birth}>"

    @staticmethod
    def hash_password(password):
        """Generate password hash from plain text password."""
        return generate_password_hash(password)

    def set_password(self, password):
        """Set the password hash for the user."""
        self.password_hash = User.hash_password(password)

    def check_password(self, password):
        """Check if the given password is correct."""
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        """Return True if the user is active."""
        return True

    def get_id(self):
        """Return the ID of the user as a string."""
        return str(self.user_id)

    @classmethod
    def create(cls, username, password, date_of_birth):
        """Create a new user."""
        user = cls(
            user_id=str(uuid.uuid4()),
            username=username,
            date_of_birth=date_of_birth,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return user

    def update(self, username=None, password=None, date_of_birth=None):
        """Update an existing user."""
        if username is not None:
            self.username = username
        if password is not None:
            self.set_password(password)
        if date_of_birth is not None:
            self.date_of_birth = date_of_birth

        db.session.commit()

    @classmethod
    def delete(cls, user):
        """Delete an existing user."""
        db.session.delete(user)
        db.session.commit()
