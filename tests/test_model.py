import os
from openai import OpenAI
from src.models import get_model, models


def test_openai_api_key_in_env():
    assert os.getenv("OPENAI_API_KEY") is not None, f"{os.getenv('OPENAI_API_KEY')=}"


def test_get_gpt3_5_model():
    model = get_model(model_name="GPT-3.5")
    assert model == models["GPT-3.5"]
    assert OpenAI().api_key[:3] == "sk-"


def test_get_gpt4_model():
    model = get_model(model_name="GPT-4")
    assert model == models["GPT-4"]
    assert OpenAI().api_key[:3] == "sk-"


def test_get_gpt4o_model():
    model = get_model(model_name="GPT-4o")
    assert model == models["GPT-4o"]
    assert OpenAI().api_key[:3] == "sk-"


def test_get_mock_model():
    model = get_model(model_name="MockModel")
    assert model == models["MockModel"]
