import openai
from src.models import get_model, models


def test_get_gpt3_5_model():
    model = get_model(model_name="gpt3.5")
    assert model == models["gpt3.5"]
    assert openai.api_key[:3] == "sk-"


def test_get_gpt4_model():
    model = get_model(model_name="gpt4")
    assert model == models["gpt4"]
    assert openai.api_key[:3] == "sk-"


def test_get_mock_model():
    model = get_model(model_name="mock")
    assert model == models["mock"]
