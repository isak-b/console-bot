from src.model import get_model, models


def test_get_gpt3_5_model(cfg):
    model = get_model(model_name="gpt3.5", env_filename=cfg["files"]["env"])
    assert model == models["gpt3.5"]


def test_get_gpt4_model(cfg):
    model = get_model(model_name="gpt4", env_filename=cfg["files"]["env"])
    assert model == models["gpt4"]


def test_get_mock_model():
    model = get_model(model_name="mock")
    assert model == models["mock"]
