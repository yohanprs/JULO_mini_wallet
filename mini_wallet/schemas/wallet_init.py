from marshmallow import Schema, fields, EXCLUDE


class WalletInitSchema(Schema):    
    customer_xid = fields.String(required=True) 

    class Meta:
        unknown = EXCLUDE