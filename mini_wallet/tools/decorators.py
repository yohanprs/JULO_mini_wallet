import functools
from functools import wraps
from typing import Any
from mini_wallet.enumerations.commons import EncodingType, SchemaMethod
from flask import current_app, g, request
from marshmallow import ValidationError
from mini_wallet.schemas.commons import BaseErrorResponseSchema

from mini_wallet.tools.responses import make_json_response


# def login_required(_func=None, *, permissions=[], token_types=[]):  # noqa
#     def decorator_login_required(func):
#         @wraps(func)
#         def wrap(*args, **kwargs):
#             auth_resource = AuthResource(
#                 base_url=current_app.config.get("AUTH_ENGINE_URL"),
#                 auth_token=None,
#             )
#             if request.headers.get("Authorization") is None:
#                 return unauthorized(errors=dict(token="Invalid token"))
#             try:
#                 auth_token = None
#                 token_result = split_token(request.headers)
#                 if token_result.status_code == 200:
#                     auth_token = token_result.data
#                 else:
#                     return unauthorized(errors=dict(token="Invalid token"))

#                 (
#                     validation_status,
#                     validation_result,
#                 ) = auth_resource.validate_general_token(
#                     auth_token=auth_token,
#                     token_types=token_types,
#                     return_permission=True,
#                 )
#             except (TypeError, UnicodeDecodeError, ValueError):
#                 return unauthorized(errors=dict(token="Invalid token"))

#             if validation_status == 200:
#                 validation_data = validation_result.get("data", {})
#                 user_permissions = validation_data.get("permissions")

#                 if not validation_data.get("token_type") == "SERVER":
#                     for permission in permissions:
#                         if permission not in user_permissions:
#                             return unauthorized(errors=dict(token="Access forbidden"))

#                 token_type = validation_data.get("token_type")
#                 if token_type == "ADMIN":
#                     g.admin_id = int(validation_data.get("user_id"))
#                 elif token_type == "USER":
#                     g.user_id = int(validation_data.get("user_id"))
#                 elif token_type == "PARTNER":
#                     g.partner_id = int(validation_data.get("partner_id"))

#                 return func(*args, **kwargs)

#             return unauthorized(errors=dict(token="Invalid token"))

#         return wrap

#     if _func is None:
#         return decorator_login_required
#     else:
#         return decorator_login_required(_func)


def validate_input(schema_method: SchemaMethod, schema, encoding_type):
    def _decorate(func: Any):
        @functools.wraps(func)
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
