import functools
import openai

from src.api import set_api_key


class MockModel:
    choices: list = [{"message": {"content": "This is a mock reply. You can change model with /change model=default"}}]

    def __call__(self, *_args, **_kwargs):
        return self


# Models
mock_model = MockModel()
gpt_3_5_turbo = functools.partial(
    openai.ChatCompletion.create,
    model="gpt-3.5-turbo",
)


def get_model(model_name: str, env_filename: str = None):
    if model_name in ["default", "gpt-3.5-turbo"]:
        set_api_key(model_name=model_name, env_filename=env_filename)
        model = gpt_3_5_turbo
    elif model_name == "mock":
        model = mock_model
    return model
