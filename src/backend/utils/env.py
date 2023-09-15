import os
from typing import Optional


def get_env(key: str, default: Optional[str] = None):
    """Get the value of an environment variable.

    :param key: The name of the environment variable.
    :param default: The default value to return if the variable is not found.
    :return: The value of the environment variable or the default value.
    """
    return os.environ.get(key, default)


def set_env(key: str, value: str):
    """Set value of an environment variable.

    :param key: The name of the environment variable.
    :param value: The value of the environment variable.
    """
    os.environ[key] = value
