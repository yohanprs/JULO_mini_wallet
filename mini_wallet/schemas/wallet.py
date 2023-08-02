
from mini_wallet.models.wallet import Wallet
from mini_wallet import ma
from mini_wallet.schemas.commons import EnumNameOnly
from marshmallow import Schema, fields, EXCLUDE


class WalletModelSchema(ma.SQLAlchemyAutoSchema):
    id = fields.UUID()
    owned_by = fields.UUID()
    status = EnumNameOnly(attribute="status")
    enabled_at = fields.DateTime(attribute = "status_change_at")
    balance = fields.Integer()    
    

    class Meta:
        model = Wallet
        exclude = ("is_deleted", "deleted_at", "created_at", "updated_at", "status_change_at")
        ordered = True

class WalletDisabledModelSchema(ma.SQLAlchemyAutoSchema):
    id = fields.UUID()
    owned_by = fields.UUID()
    status = EnumNameOnly(attribute="status")
    disabled_at = fields.DateTime(attribute = "status_change_at")
    balance = fields.Integer()    
    

    class Meta:
        model = Wallet
        exclude = ("is_deleted", "deleted_at", "created_at", "updated_at", "status_change_at")
        ordered = True

class WalletDisableSchema(Schema):    
    is_disabled = fields.Boolean(required=True) 

    class Meta:
        unknown = EXCLUDE