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


def ok_message(status: str = None, data: dict = {}) -> Tuple[int, dict]:
    return (
        200,
        dict(           
            status=status if status else "success",
            data=data,
        )
    )   


def created_message(status: str = None, data: dict = {}) -> Tuple[int, dict]:
    return (
        201,
        dict(           
            status=status if status else "success",
            data=data,
        )       
    )


def bad_request_message(status: str = None, error: str = "bad request") -> Tuple[int, dict]:
    
    return (
        400,       
        dict(           
            status=status if status else "fail",
            data=dict(error=error)
        )    
    )



def not_found_response(status: str = None, error: str = "not found") -> Tuple[int, dict]:
    return (
        404,
        dict(           
            status=status if status else "fail",
            data=dict(error=error)
        )
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
