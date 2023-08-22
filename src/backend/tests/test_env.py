from utils.env import get_env
import os


def fake_env():
    os.environ["API_KEY"] = "SOMETHING"


def test_env():
    fake_env()
    assert (get_env("API_KEY")) == "SOMETHING"
    assert (get_env("NOT_EXISTED", "DEFAULT")) == "DEFAULT"
