import functools
import openai

from api import load_openai_api_key


class MockModel:
    content = "This is a mock reply.\nYou can change to the default model with /config model=default"
    choices: list = [{"message": {"role": "assistant", "content": content}}]

    def __call__(self, *_args, **_kwargs):
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
    if model_name != "mock":
        load_openai_api_key(env_filename=env_filename)
    return model
