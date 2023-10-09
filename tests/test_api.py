import openai

from src.api import load_openai_api_key


def test_load_openai_api_key(cfg):
    load_openai_api_key(env_filename=cfg["files"]["env"])
    assert openai.api_key is not None
    assert openai.api_key[:3] == "sk-"
