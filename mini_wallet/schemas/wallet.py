
from mini_wallet.models.wallet import Wallet
from mini_wallet import ma
from mini_wallet.schemas.commons import EnumNameOnly
from marshmallow import fields


class WalletModelSchema(ma.SQLAlchemyAutoSchema):
    id = fields.UUID()
    owned_by = fields.UUID()
    status = EnumNameOnly(attribute="status")
    enabled_at = fields.DateTime()
    balance = fields.Integer()    
    

    class Meta:
        model = Wallet
        exclude = ("is_deleted", "deleted_at", "created_at", "updated_at")
        ordered = True