import functools
import openai

from api import set_api_key


class MockModel:
    choices: list = [
        {
            "message": {
                "role": "assistant",
                "content": "This is a mock reply. You can change to the default model with /config model=default",
            }
        }
    ]

    def __call__(self, *_args, **_kwargs):
        return self


# Models
mock_model = MockModel()
gpt3_5 = functools.partial(
    openai.ChatCompletion.create,
    model="gpt-3.5-turbo",
)
gpt4 = functools.partial(
    openai.ChatCompletion.create,
    model="gpt-4",
)


def get_model(model_name: str, env_filename: str = None):
    if model_name in ["default", "gpt3.5"]:
        set_api_key(model_name=model_name, env_filename=env_filename)
        model = gpt3_5
    elif model_name == "gpt4":
        set_api_key(model_name=model_name, env_filename=env_filename)
        model = gpt4
    elif model_name == "mock":
        model = mock_model
    return model
