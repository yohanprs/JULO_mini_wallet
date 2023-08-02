import sqlalchemy as sa

from mini_wallet.enumerations.wallet import WalletStatus
from .base_model import BaseModel
from sqlalchemy.orm import relationship


class Wallet(BaseModel):
    __tablename__ = "wallet"
        
    owned_by = sa.Column(sa.String(36), nullable=False, unique=True)
    balance = sa.Column(sa.Integer())
    status = sa.Column(sa.Enum(WalletStatus, name="wallet_status"))
    status_change_at = sa.Column(sa.DateTime(), nullable=True)
    transactions = relationship("Transaction", uselist=True, back_populates="wallet")