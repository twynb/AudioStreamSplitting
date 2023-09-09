import os

from src.backend.utils.env import get_env, set_env


def fake_env():
    os.environ["ACOUSTID_API_KEY"] = "SOMETHING"


def test_env():
    fake_env()
    assert (get_env("ACOUSTID_API_KEY")) == "SOMETHING"
    assert (get_env("NOT_EXISTED", "DEFAULT")) == "DEFAULT"
    set_env("ACOUSTID_API_KEY", "CHANGED")
    assert (get_env("ACOUSTID_API_KEY")) == "CHANGED"
