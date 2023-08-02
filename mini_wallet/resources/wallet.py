from flask import Response, g
from flask_restful import Resource
from mini_wallet.controllers.wallet import WalletController
from mini_wallet.enumerations.commons import EncodingType, SchemaMethod
from mini_wallet.schemas.wallet import WalletDisableSchema
from mini_wallet.tools.decorators import login_required, validate_input
from mini_wallet.tools.responses import make_json_response


class WalletResource(Resource):
    @login_required()
    def post(self, **kwargs) -> Response:
        status, result = WalletController().enable_wallet(g.customer_xid)

        return make_json_response(status, result)
    
    @login_required()
    def get(self, **kwargs) -> Response:
        status, result = WalletController().view_wallet(g.customer_xid)

        return make_json_response(status, result)
    
    @login_required()
    @validate_input(SchemaMethod.LOAD, WalletDisableSchema(), EncodingType.FORMDATA)
    def patch(self, **kwargs) -> Response:
        is_disabled = kwargs.get("is_disabled")        

        status, result = WalletController().disable_wallet(g.customer_xid, is_disabled)

        return make_json_response(status, result)