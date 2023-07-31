from enum import Enum


class TransactionStatus(Enum):
    success = "success"
    failed = "failed"

class TransactionType(Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"