import os
import functools

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class MockModel:
    """Mock model for testing purposes (doesn't use up API tokens)"""

    class Message:
        def __init__(self, role, content):
            self.role = role
            self.content = content

    class Choice:
        def __init__(self, message):
            self.message = message

    def __init__(self):
        self.keywords = {"model": "mock-model"}

    def __call__(self, *_args, **_kwargs):
        self.content = f"This is just a mock reply"
        self.choices = [self.Choice(self.Message(role="assistant", content=self.content))]
        return self


def get_openai_models(include_chat: bool = True, chat_prefixes: list = ["gpt-3.5", "gpt-4"]) -> dict:
    """Get OpenAI models"""
    assert os.getenv("OPENAI_API_KEY") is not None, f"Environment variable 'OPENAI_API_KEY' has not been set."
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    all_models = client.models.list().data
    models = {}
    if include_chat is True:
        models["chat"] = {}
        for model in all_models:
            if any(model.id.startswith(prefix) for prefix in chat_prefixes):
                models["chat"][model.id] = functools.partial(client.chat.completions.create, model=model.id)
    return models


def get_mock_models(include_chat: bool = True):
    """Get mock models"""
    models = {}
    if include_chat is True:
        models["chat"] = {"mock-model": MockModel()}
    return models


def get_models(include_chat: bool = True, include_openai: bool = True, include_mock: bool = True) -> dict:
    """Get models as a dict"""
    models = {}
    if include_openai is True:
        openai_models = get_openai_models(include_chat=include_chat)
        for key, val in openai_models.items():
            models[key] = val if key not in models else {**models[key], **val}
    if include_mock is True:
        mock_models = get_mock_models(include_chat=include_chat)
        for key, val in mock_models.items():
            models[key] = val if key not in models else {**models[key], **val}
    return models
