import os
from openai import OpenAI
from src.models import get_model, models


def test_openai_api_key_in_env():
    assert os.getenv("OPENAI_API_KEY") is not None, f"{os.getenv('OPENAI_API_KEY')=}"


def test_get_gpt3_5_model():
    model = get_model(model_name="gpt-35")
    assert model == models["gpt-35"]
    assert OpenAI().api_key[:3] == "sk-"


def test_get_gpt4_model():
    model = get_model(model_name="gpt-4")
    assert model == models["gpt-4"]
    assert OpenAI().api_key[:3] == "sk-"


def test_get_gpt4o_model():
    model = get_model(model_name="gpt-4o")
    assert model == models["gpt-4o"]
    assert OpenAI().api_key[:3] == "sk-"


def test_get_mock_model():
    model = get_model(model_name="mock")
    assert model == models["mock"]
