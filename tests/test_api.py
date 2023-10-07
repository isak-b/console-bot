import openai

from src.api import set_api_key, _load_openai_api_key


def test_load_openai_api_key(cfg):
    _load_openai_api_key(env_filename=cfg["files"]["env"])
    assert openai.api_key is not None
    assert openai.api_key[:3] == "sk-"


def test_set_api_key(cfg):
    set_api_key(model_name="default", env_filename=cfg["files"]["env"])
    assert openai.api_key is not None
    assert openai.api_key[:3] == "sk-"
