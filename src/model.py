import functools
import openai

from api import load_openai_api_key


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


def get_model(model_name: str, env_filename: str = None):
    model = models[model_name]
    if model_name in ["gpt3.5", "gpt4"]:
        load_openai_api_key(env_filename=env_filename)
    return model
