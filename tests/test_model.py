import os

from src.models import get_models, get_openai_models, get_mock_models


def test_openai_api_key_in_env():
    assert os.getenv("OPENAI_API_KEY") is not None, f"{os.getenv('OPENAI_API_KEY')=}"


def test_get_chat_models():
    # True
    models_with_chat = get_models(include_chat=True)
    assert "chat" in models_with_chat
    assert len(models_with_chat["chat"]) > 0

    # False
    models_without_chat = get_models(include_chat=False)
    assert "chat" not in models_without_chat


def test_get_openai_models():
    test_models = {"chat": ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4o"]}
    all_models_with_openai = get_models(include_chat=True, include_openai=True)
    all_models_without_openai = get_models(include_chat=True, include_openai=False)
    openai_models = get_openai_models(include_chat=True)
    for model_type, expected_models in test_models.items():
        for expected_model in expected_models:

            # Included
            assert expected_model in all_models_with_openai[model_type]
            assert expected_model in openai_models[model_type]
            assert all_models_with_openai[model_type][expected_model].keywords["model"] == expected_model
            assert all_models_with_openai[model_type][expected_model].keywords["model"] == expected_model

            # Not included
            assert expected_model not in all_models_without_openai[model_type]


def test_get_mock_models():
    test_models = {"chat": ["mock-model"]}
    all_models_with_mock = get_models(include_chat=True, include_mock=True)
    all_models_without_mock = get_models(include_chat=True, include_mock=False)
    mock_models = get_mock_models(include_chat=True)
    for model_type, expected_models in test_models.items():
        for expected_model in expected_models:

            # Included
            assert expected_model in all_models_with_mock[model_type]
            assert expected_model in mock_models[model_type]
            assert all_models_with_mock[model_type][expected_model].keywords["model"] == expected_model
            assert mock_models[model_type][expected_model].keywords["model"] == expected_model

            # Not included
            assert expected_model not in all_models_without_mock[model_type]
