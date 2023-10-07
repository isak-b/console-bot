import functools
import openai

from api import set_api_key

gpt3_5_standard = functools.partial(
    openai.ChatCompletion.create,
    model="gpt-3.5-turbo",
)


class MockModel:
    choices: list = [{"message": {"content": "This is a mock reply. You can change model with /change model=default"}}]

    def __call__(self, *_args, **_kwargs):
        return self


def get_model(model_name: str, env_filename: str):
    if model_name in ["default", "gpt3_5_standard"]:
        set_api_key(model_name=model_name, env_filename=env_filename)
        model = gpt3_5_standard
    elif model_name == "mock":
        model = MockModel()
    return model
