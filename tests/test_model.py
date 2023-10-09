from src.model import get_model, gpt3_5, gpt4, mock_model


def test_get_gpt3_5_model(cfg):
    model = get_model(model_name="gpt3.5", env_filename=cfg["files"]["env"])
    assert model == gpt3_5


def test_get_gpt4_model(cfg):
    model = get_model(model_name="gpt4", env_filename=cfg["files"]["env"])
    assert model == gpt4


def test_get_mock_model():
    model = get_model(model_name="mock")
    assert model == mock_model
