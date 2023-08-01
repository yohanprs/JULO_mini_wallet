from datetime import datetime
import functools
from functools import wraps
from typing import Any
from mini_wallet import unauthorized
from mini_wallet.enumerations.commons import EncodingType, SchemaMethod
from flask import current_app, g, request
from marshmallow import ValidationError
from mini_wallet.models.customer_token import CustomerToken
from mini_wallet.schemas.commons import BaseErrorResponseSchema

from mini_wallet.tools.responses import make_json_response

def login_required():  # noqa
    def decorator_login_required(func: Any):
        @wraps(func)
        def wrap(*args, **kwargs):            
            if request.headers.get("Authorization") is None:
                return unauthorized("Invalid token")
            
            auth_token = None
            
            allowed_auth_type = ["bearer", "jwt", "token"]
            auth_header = request.headers.get("Authorization", request.headers.get("authorization"))
            auth_type, auth_token = (
                auth_header.split() if auth_header is not None else (None, None)
            )
            if not all([auth_type, auth_token]) or auth_type.lower() not in allowed_auth_type:
                return unauthorized("Invalid token")            
            
            if not auth_token:
                return unauthorized("Invalid token")
            
            current_time = datetime.utcnow()
            existing_token = CustomerToken.base_query().filter(
                CustomerToken.token==auth_token, 
                CustomerToken.is_active==True, 
                CustomerToken.expires > current_time
            ).first()

            if not existing_token:
                return unauthorized("Invalid token")
            
            g.customer_xid = existing_token.customer_xid

            return func(*args, **kwargs)

        return wrap
   
    return decorator_login_required


def validate_input(schema_method: SchemaMethod, schema, encoding_type):
    def _decorate(func: Any):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                data = None
                match encoding_type:
                    case EncodingType.PARAM:
                        data = request.args.to_dict()

                    case EncodingType.JSON:
                        data = request.get_json()

                    case EncodingType.FORMDATA:
                        data = request.form.to_dict()

                if encoding_type == EncodingType.FORMDATA and request.files:
                    for field_name in request.files.keys():
                        data[field_name] = request.files[field_name]

                if kwargs:
                    data.update(kwargs)

            except Exception as e:
                return make_json_response(status_code=500, data={"code": 500, "message": str(e)})

            try:
                mapping_function = {
                    SchemaMethod.LOAD: schema.load,
                    SchemaMethod.VALIDATE: schema.validate,
                }
                data = mapping_function[schema_method](data)
            except ValidationError as e:
                response = BaseErrorResponseSchema().dump(
                    {
                        "code": 400,
                        "message": "Bad Request",
                        "errors": e.normalized_messages(),
                    }
                )
                return make_json_response(status_code=400, data=response)

            kwargs.update(data)

            return func(*args, **kwargs)

        return wrapper

    return _decorate
