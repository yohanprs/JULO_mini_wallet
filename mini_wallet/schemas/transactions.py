from mini_wallet import ma
from marshmallow import Schema, fields, EXCLUDE

from mini_wallet.models.transaction import Transaction
from mini_wallet.schemas.commons import EnumNameOnly

class TransactionsDepositSchema(Schema):
    amount = fields.Integer(as_string=True, required=True)
    reference_id = fields.UUID(required=True)

    class Meta:
        unknown = EXCLUDE


class TransactionsWithdrawalSchema(Schema):
    amount = fields.Integer(as_string=True, required=True)
    reference_id = fields.UUID(required=True)

    class Meta:
        unknown = EXCLUDE

class DepositTransactionModelSchema(ma.SQLAlchemyAutoSchema):
    id = fields.UUID()
    deposited_by = fields.UUID(attribute="wallet_owned_by")
    status = EnumNameOnly(attribute="status")
    deposited_at = fields.DateTime(attribute="transacted_at")
    amount = fields.Integer()
    reference_id = fields.UUID()  
    

    class Meta:
        model = Transaction
        exclude = ("is_deleted", "deleted_at", "created_at", "updated_at", "transacted_at", "type")
        ordered = True

class WithdrawalTransactionModelSchema(ma.SQLAlchemyAutoSchema):
    id = fields.UUID()
    withdrawn_by = fields.UUID(attribute="wallet_owned_by")
    status = EnumNameOnly(attribute="status")
    withdrawn_at = fields.DateTime(attribute="transacted_at")
    amount = fields.Integer()
    reference_id = fields.UUID()  
    

    class Meta:
        model = Transaction
        exclude = ("is_deleted", "deleted_at", "created_at", "updated_at", "transacted_at", "type")
        ordered = True

