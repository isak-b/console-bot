from src.model import get_model, gpt_3_5_turbo, mock_model


def test_get_default_model(cfg):
    model = get_model(model_name="default", env_filename=cfg["files"]["env"])
    assert model == gpt_3_5_turbo


def test_get_mock_model():
    model = get_model(model_name="mock")
    assert model == mock_model
