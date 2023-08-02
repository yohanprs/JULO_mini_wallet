from flask import Response, g
from flask_restful import Resource
from mini_wallet.controllers.transaction import TransactionController
from mini_wallet.controllers.wallet import WalletController
from mini_wallet.enumerations.commons import EncodingType, SchemaMethod
from mini_wallet.schemas.transactions import GetTransactionListSchema
from mini_wallet.tools.decorators import login_required, validate_input
from mini_wallet.tools.responses import make_json_response


class TransactionsResource(Resource):

    @login_required()
    @validate_input(SchemaMethod.LOAD, GetTransactionListSchema(), EncodingType.PARAM)
    def get(self, **kwargs) -> Response:
        status, result = TransactionController().get_transactions_list(g.customer_xid, **kwargs)

        return make_json_response(status, result)