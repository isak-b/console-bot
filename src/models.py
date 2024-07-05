import os
import functools
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class MockModel:
    """Mock model for testing purposes, it doesn't use up API tokens."""

    class Message:
        def __init__(self, role, content):
            self.role = role
            self.content = content

    class Choice:
        def __init__(self, message):
            self.message = message

    def __init__(self):
        self.content = "This is just a mock reply"
        self.choices = [self.Choice(self.Message(role="assistant", content=self.content))]

    def __call__(self, *_args, **_kwargs):
        import time

        time.sleep(1.5)
        return self


gpt_35 = functools.partial(
    OpenAI(api_key=os.getenv("OPENAI_API_KEY")).chat.completions.create,
    model="gpt-3.5-turbo",
)
gpt_4 = functools.partial(
    OpenAI(api_key=os.getenv("OPENAI_API_KEY")).chat.completions.create,
    model="gpt-4-turbo",
)
gpt_4o = functools.partial(
    OpenAI(api_key=os.getenv("OPENAI_API_KEY")).chat.completions.create,
    model="gpt-4o",
)
models = {
    "GPT-3.5": gpt_35,
    "GPT-4": gpt_4,
    "GPT-4o": gpt_4o,
    "MockModel": MockModel(),
}


def get_model(model_name: str):
    """Get model object by name"""
    model = models[model_name]
    return model
