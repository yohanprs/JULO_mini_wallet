"""
This file handle commons schemas
"""
from datetime import datetime
from enum import Enum

from mini_wallet import ma
from marshmallow import fields


class BaseResponseSchema(ma.Schema):
    """
    This class is base schema for API response
    """

    code = fields.Integer()
    message = fields.String()
    timestamp = fields.DateTime(default=datetime.now())

    class Meta:
        """
        This class handle Meta of Base response schema
        """
        ordered = True


class BaseErrorResponseSchema(BaseResponseSchema):
    """
    This class is base schema for API error response
    """

    errors = fields.Raw()    


class EnumToDictionary(fields.Field):
    """Field that serializes enum to dict"""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if isinstance(value, Enum):
            return {"name": value.name, "value": value.value}
        else:
            return value


class EnumNameOnly(fields.Field):
    """Field that serializes enum to string"""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if isinstance(value, Enum):
            return value.name


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(ma.Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


class DefaultResponseSchema(BaseResponseSchema):
    """
    This class is basic response which doesn't require
    ma.Schema
    """
    data = fields.Dict(default={})


class LowerCased(fields.Field):
    """
    Field that deserialize to lower case
    """
    def _deserialize(self, value, attr, data, **kwargs):
        return value.lower()


class GetListSchema(ma.Schema):
    offset = fields.Integer()
    limit = fields.Integer()


class GetListSchemaWithKeyword(GetListSchema):
    keywords = fields.String()
