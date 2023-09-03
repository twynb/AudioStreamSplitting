import os

from utils.env import get_env, set_env


def fake_env():
    os.environ["API_KEY"] = "SOMETHING"


def test_env():
    fake_env()
    assert (get_env("API_KEY")) == "SOMETHING"
    assert (get_env("NOT_EXISTED", "DEFAULT")) == "DEFAULT"
    set_env("API_KEY", "CHANGED")
    assert (get_env("API_KEY")) == "CHANGED"
