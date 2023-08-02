import uuid
from mini_wallet.enumerations.transaction import TransactionStatus, TransactionType
from .base_model import BaseModel
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

class Transaction(BaseModel):
    __tablename__ = "transaction"

    wallet_id = sa.Column(sa.String(36), sa.ForeignKey("wallet.id"), nullable=False)
    status = sa.Column(sa.Enum(TransactionStatus, name="transaction_status"), nullable=False)
    transacted_at = sa.Column(sa.DateTime(), nullable=False)
    type = sa.Column(sa.Enum(TransactionType, name="transaction_type"), nullable=False)
    amount = sa.Column(sa.Integer())
    reference_id = sa.Column(sa.String(36), unique=True)
    wallet = relationship("Wallet", back_populates="transactions")

    @hybrid_property
    def wallet_owned_by(self):
        return self.wallet.owned_by
        
