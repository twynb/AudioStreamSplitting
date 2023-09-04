import os
from typing import Optional

from utils.path import get_abs_src_dir_in_built_app


def load_env():
    """Load environment variables from a file into os.environ.
    This will be called immediately.
    """
    file_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(file_path):
        file_path = os.path.join(get_abs_src_dir_in_built_app(), ".env")

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("VITE"):
                key, value = line.split("=", 1)
                os.environ[key] = value


load_env()


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
