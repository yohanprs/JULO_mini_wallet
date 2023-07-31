"""
This class is used to manage environment variable
"""

from functools import partial
from os import getenv
from typing import Any, Callable


def get_env(
    prefix: str, env_name: str, default: Any, var_type: Callable[[str], Any] = str
) -> Any:
    value = getenv(f"{prefix}_{env_name}")

    if not value:
        return var_type(default)

    return var_type(value)


_str = partial(get_env, var_type=str)


def _bool(prefix: str, varname: str, default: bool = None) -> bool:
    return get_env(prefix, varname, default, lambda x: x in ["1", "true", "t", True])


def _int(prefix: str, varname: str, default: int = None) -> int:
    return get_env(prefix, varname, default, int)


class EnvConfig:
    def __init__(self, app_prefix: str):
        self.app_prefix = app_prefix

    def boolean(self, varname: str, default: Any = None) -> bool:
        return _bool(self.app_prefix, varname, default)

    def string(self, varname: str, default: str = None) -> str:
        return _str(self.app_prefix, varname, default)

    def int(self, varname: str, default: int = None) -> int:
        return _int(self.app_prefix, varname, default)