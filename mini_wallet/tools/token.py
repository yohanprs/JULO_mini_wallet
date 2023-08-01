
from datetime import datetime, timedelta
from flask import current_app
import jwt


def create_user_token(customer_xid):
    # simple token creation for exercise
    token_expire_in_hours = current_app.config.get("TOKEN_EXPIRE")
    secret = current_app.config.get("SECRET_TOKEN")

    token_expire = datetime.utcnow() + timedelta(hours=token_expire_in_hours)

    payload = dict()    
    payload["customer_xid"] = customer_xid
    payload["expires"] = str(token_expire)   

    token = jwt.encode(payload, secret, algorithm="HS256")
    return token_expire, token