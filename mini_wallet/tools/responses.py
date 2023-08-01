"""
This file handle tools for API response
"""
import json
from http import HTTPStatus
from typing import Tuple
from flask import Response
from mini_wallet.schemas.commons import BaseErrorResponseSchema, DefaultResponseSchema


def make_json_response(status_code: int, data: dict) -> Response:
    status = {status.value: status for status in HTTPStatus}.get(status_code)
    return Response(
        response=json.dumps(data),
        status=status,
        mimetype="application/json",
    )


def unauthorized() -> Response:
    """
    This method used to make unauthorized API response

    Returns:
        Response -- [flask Response object]
    """
    data = BaseErrorResponseSchema().dump({"message": "Unauthorized"})
    return make_json_response(status_code=401, data=data)


def default_response(status_code: int, response_data):
    pass


def ok_message(message: str = None, data: dict = {}) -> Tuple[int, dict]:
    return (
        200,
        DefaultResponseSchema().dump(dict(code=200, message=message if message else "Ok", data=data)),
    )   


def created_message(status: str = None, data: dict = {}) -> Tuple[int, dict]:
    return (
        201,
        dict(           
            status=status if status else "success",
            data=data,
        )       
    )


def bad_request_message(message: str = None, field_name: str = "message") -> Tuple[int, dict]:
    errors_dict = dict()
    errors_dict[field_name] = [message]

    return (
        400,       
        BaseErrorResponseSchema().dump(dict(code=400, message="Bad request", errors=errors_dict)),
    )


def bad_request_custom_message(message: str = None) -> Tuple[int, dict]:
    return (
        400,
        BaseErrorResponseSchema().dump(dict(code=400, message=message)),
    )


def not_found_response(message: str = None) -> Tuple[int, dict]:
    return (
        404,
        BaseErrorResponseSchema().dump(
            dict(
                code=404,
                message="Not found",
                errors=dict(message=message),
            )
        ),
    )


def unprocessable_entity_response(message: str = "") -> Tuple[int, dict]:
    return (
        422,
        BaseErrorResponseSchema().dump(
            dict(
                code=422,
                message="Unprocessable entity",
                errors=dict(message=message),
            )
        ),
    )


def internal_error_response(message: str = None) -> Tuple[int, dict]:
    return (
        500,
        BaseErrorResponseSchema().dump(
            dict(
                code=500,
                message="Internal server error",
                errors=dict(message=message),
            )
        ),
    )
