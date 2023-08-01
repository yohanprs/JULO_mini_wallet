from enum import Enum


class SchemaMethod(Enum):
    LOAD = "Load"
    DUMP = "Dump"
    VALIDATE = "Validate"


class EncodingType(Enum):
    JSON = "Json"
    PARAM = "Param"
    FORMDATA = "Formdata"
