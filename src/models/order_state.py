from enum import Enum


class OrderState(Enum):
    SUBMITTED = 'submitted'
    PENDING = 'pending'
    COMPLETED = 'completed'
