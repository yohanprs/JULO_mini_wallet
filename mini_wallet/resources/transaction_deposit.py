from flask import Response, g
from flask_restful import Resource
from mini_wallet.controllers.transaction import TransactionController
from mini_wallet.enumerations.commons import EncodingType, SchemaMethod
from mini_wallet.enumerations.transaction import TransactionType
from mini_wallet.schemas.transactions import TransactionsDepositSchema
from mini_wallet.tools.decorators import login_required,validate_input
from mini_wallet.tools.responses import make_json_response


class TransactionsDepositResource(Resource):   
    @login_required()
    @validate_input(SchemaMethod.LOAD, TransactionsDepositSchema(), EncodingType.FORMDATA)
    def post(self, **kwargs) -> Response:
        status, result = TransactionController().do_transaction(g.customer_xid, TransactionType.deposit, **kwargs)

        return make_json_response(status, result)