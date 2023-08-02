from flask import Blueprint
from flask_restful import Api
from mini_wallet.resources.transaction_deposit import TransactionsDepositResource
from mini_wallet.resources.transaction_withdrawal import TransactionsWithdrawalResource
from mini_wallet.resources.wallet import WalletResource

from mini_wallet.resources.wallet_init import WalletInitResource

wallet_blueprint = Blueprint("wallet", __name__, url_prefix="/api/v1")

wallet_resources = Api(wallet_blueprint)

wallet_resources.add_resource(WalletInitResource, "/init")
wallet_resources.add_resource(WalletResource, "/wallet")
# wallet_resources.add_resource(TransactionsResource, "/wallet/transactions")
wallet_resources.add_resource(TransactionsDepositResource, "/wallet/deposits")
wallet_resources.add_resource(TransactionsWithdrawalResource, "/wallet/withdrawals")