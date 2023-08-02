from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from mini_wallet import db
from mini_wallet.enumerations.transaction import TransactionStatus, TransactionType
from mini_wallet.enumerations.wallet import WalletStatus
from mini_wallet.models.transaction import Transaction
from mini_wallet.models.wallet import Wallet
from mini_wallet.schemas.transactions import DepositTransactionModelSchema, TransactionModelSchema, WithdrawalTransactionModelSchema
from mini_wallet.tools.responses import bad_request_message, created_message, not_found_response, ok_message


class TransactionController:

    def get_transactions_list(self, customer_xid, offset=0, limit=100):

        trans_query = Transaction.base_query().join(Transaction.wallet).filter(Wallet.owned_by==customer_xid).order_by(Transaction.transacted_at)
        if offset:
            trans_query = trans_query.offset(offset)
        if limit:
            trans_query = trans_query.limit(limit)

        transaction_list = trans_query.all()

        return ok_message(data={"transactions": TransactionModelSchema().dump(transaction_list, many=True)})



    def get_wallet_by_customer_xid(self, customer_xid):
        existing_wallet = Wallet.base_query().filter(Wallet.owned_by==customer_xid).first()
        return existing_wallet

    def do_transaction(self, customer_xid, trans_type:TransactionType, **kwargs):
        amount = kwargs.get("amount")
        reference_id = kwargs.get("reference_id")

        existing_wallet = self.get_wallet_by_customer_xid(customer_xid)
        if not existing_wallet:
            return bad_request_message(error="wallet not exist")
        
        if existing_wallet.status == WalletStatus.disabled:
            return not_found_response(error="Wallet disabled")
        
        new_trans = None
        try:
            # update wallet balance
            wallet_trans = TransactionFactory.get_transaction(trans_type)

            new_trans = wallet_trans.execute_transaction(customer_xid, amount, reference_id)

        except Exception as e:
            return bad_request_message(error=str(e))     

        return created_message(data=wallet_trans.serialize_output(new_trans))  


        


class BaseTransaction(ABC):
    @abstractmethod
    def execute_transaction(self, customer_xid, amount, reference_id) -> Transaction:
        pass

    @abstractmethod
    def serialize_output(self, output_transaction:Transaction):
        pass

class TransactionFactory:
    @staticmethod
    def get_transaction(trans_type: TransactionType) -> BaseTransaction:
        trans: BaseTransaction = None
        match trans_type:
            case TransactionType.deposit:
                trans = DepositTransaction()
            case TransactionType.withdrawal:
                trans = WithdrawalTransaction()            
            case _:
                raise NotImplementedError(
                    f"Transaction with type: {trans_type.name} not yet implemented"
                )
        return trans
    


class DepositTransaction(BaseTransaction):
    def execute_transaction(self, customer_xid, amount, reference_id):
        try:
            # lock wallet for the customer
            existing_wallet = Wallet.base_query().filter(Wallet.owned_by==customer_xid).with_for_update().first()

            # create transaction
            trans = Transaction()
            trans.wallet_id = existing_wallet.id
            trans.amount = amount
            trans.reference_id = reference_id
            trans.type = TransactionType.deposit
            trans.status = TransactionStatus.success
            trans.transacted_at = datetime.utcnow()
            db.session.add(trans)

            # update wallet balance
            existing_wallet.balance += amount
            db.session.add(existing_wallet)

            # Insert additional process here if required

            db.session.commit()
        except IntegrityError as ie:
            db.session.rollback()
            if ie.orig.pgerror.find("reference_id") != -1:
                raise Exception(f"there is another transaction with same reference id")
            else:
                raise ie
        except Exception as e:
            db.session.rollback()
            raise e

        return trans
    
    def serialize_output(self, output_transaction:Transaction):
        return {"deposit": DepositTransactionModelSchema().dump(output_transaction)}
    
class WithdrawalTransaction(BaseTransaction):
    def execute_transaction(self, customer_xid, amount, reference_id):
        try:
            # lock wallet for the customer
            existing_wallet = Wallet.base_query().filter(Wallet.owned_by==customer_xid).with_for_update().first()

            valid_withdrawal = True
            # check balance
            if existing_wallet.balance < amount:
                valid_withdrawal = False

            # create transaction
            trans = Transaction()
            trans.wallet_id = existing_wallet.id
            trans.amount = amount
            trans.reference_id = reference_id
            trans.type = TransactionType.withdrawal
            if valid_withdrawal:
                trans.status = TransactionStatus.success
            else:
                trans.status = TransactionStatus.failed
            trans.transacted_at = datetime.utcnow()
            db.session.add(trans)

            if valid_withdrawal:
                # update wallet balance
                existing_wallet.balance -= amount
                db.session.add(existing_wallet)

            # Insert additional process here if required

            db.session.commit()

            if not valid_withdrawal:
                raise Exception("balance not enough for withdrawal")
        except IntegrityError as ie:
            db.session.rollback()
            if ie.orig.pgerror.find("reference_id") != -1:
                raise Exception(f"there is another transaction with same reference id")
            else:
                raise ie
        except Exception as e:
            db.session.rollback()
            raise e

        return trans
    
    def serialize_output(self, output_transaction:Transaction):
        return {"withdrawal": WithdrawalTransactionModelSchema().dump(output_transaction)}
            
        

        

        
