from datetime import datetime, timedelta

from flask import current_app
from mini_wallet import db
from mini_wallet.enumerations.wallet import WalletStatus
from mini_wallet.models.customer_token import CustomerToken
from mini_wallet.models.wallet import Wallet
from mini_wallet.schemas.wallet import WalletModelSchema
from mini_wallet.tools.responses import bad_request_message, created_message
from mini_wallet.tools.token import create_user_token


class WalletController:
    """
    This class is controller for wallet
    """

    def validate_customer_xid(self, customer_xid):
        # Validate customer xid here for a real system

        # for exercise, assume customer xid is valid
        return True

    def init_wallet(self, customer_xid):

        valid = self.validate_customer_xid(customer_xid)

        if not valid:
            raise Exception("invalid customer_xid")
        
        user_token = ""
        with db.session.begin():
            # check if wallet for the customer already exist
            existing_wallet = Wallet.base_query().filter(Wallet.owned_by==customer_xid).first()

            # if not create one
            if not existing_wallet:
                existing_wallet = Wallet()
                existing_wallet.owned_by = customer_xid
                existing_wallet.balance = 0
                existing_wallet.status = WalletStatus.disabled
                db.session.add(existing_wallet)

            # check if customer token already exist, active and not expire
            current_time = datetime.utcnow()
            existing_token = CustomerToken.base_query().filter(
                CustomerToken.customer_xid==customer_xid, 
                CustomerToken.is_active==True, 
                CustomerToken.expires > current_time
            ).first()

            # if not create new token
            if not existing_token:
                token_expire, token = create_user_token(customer_xid)
                existing_token = CustomerToken()
                existing_token.customer_xid = customer_xid
                existing_token.is_active = True
                existing_token.expires = token_expire
                existing_token.token = token
                db.session.add(existing_token)

            user_token = existing_token.token

        # return new token and status
        return created_message(data={"token": user_token})
    
    def enable_wallet(self, customer_xid):
        # check if wallet for the customer already exist
        existing_wallet = Wallet.base_query().filter(Wallet.owned_by==customer_xid).first()
        if not existing_wallet:
            return bad_request_message(error="wallet not exist")
        
        if existing_wallet.status == WalletStatus.enabled:
            return bad_request_message(error="Already enabled")
        
        existing_wallet.status = WalletStatus.enabled
        existing_wallet.enabled_at = datetime.utcnow()
        existing_wallet.save()

        return created_message(data={"wallet": WalletModelSchema().dump(existing_wallet)})
        





    

