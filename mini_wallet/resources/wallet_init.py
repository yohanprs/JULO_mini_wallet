from flask import Response
from flask_restful import Resource
from mini_wallet.controllers.wallet import WalletController

from mini_wallet.enumerations.commons import EncodingType, SchemaMethod
from mini_wallet.schemas.wallet_init import WalletInitSchema
from mini_wallet.tools.decorators import validate_input
from mini_wallet.tools.responses import make_json_response


class WalletInitResource(Resource):   
    @validate_input(SchemaMethod.LOAD, WalletInitSchema(), EncodingType.FORMDATA)
    def post(self, **kwargs) -> Response:
        status, result = WalletController().init_wallet(kwargs.get("customer_xid"))

        return make_json_response(status, result)