import os
import functools
import openai
from dotenv import load_dotenv


class MockModel:
    msg = "This is just a mock reply (set model: /cfg model=default)"
    choices: list = [{"message": {"role": "assistant", "content": msg}}]

    def __call__(self, messages, *_args, **_kwargs):
        self.choices = [{"message": {"role": "assistant", "content": f"{self.msg}. You: {messages[-1]['content']}"}}]
        return self


gpt3_5 = functools.partial(
    openai.ChatCompletion.create,
    model="gpt-3.5-turbo",
)
gpt4 = functools.partial(
    openai.ChatCompletion.create,
    model="gpt-4",
)
models = {
    "default": gpt3_5,
    "mock": MockModel(),
    "gpt3.5": gpt3_5,
    "gpt4": gpt4,
}


def get_model(model_name: str):
    model = models[model_name]
    if model_name in ["default", "gpt3.5", "gpt4"]:
        if not openai.api_key:
            load_dotenv()
            openai.api_key = os.getenv("OPENAI_API_KEY")
    return model
