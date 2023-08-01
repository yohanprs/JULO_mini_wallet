import sqlalchemy as sa
from .base_model import BaseModel


class CustomerToken(BaseModel):
    __tablename__ = "customer_token"

    customer_xid = sa.Column(sa.String(36), nullable=False)
    token = sa.Column(sa.String(210), nullable=False)
    expires = sa.Column(sa.DateTime())
    is_active = sa.Column(sa.Boolean())