import os
import functools
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class MockModel:
    msg = "This is just a mock reply (set model: /cfg model=default)"
    choices: list = [{"message": {"role": "assistant", "content": msg}}]

    def __call__(self, messages, *_args, **_kwargs):
        self.choices = [{"message": {"role": "assistant", "content": f"{self.msg}. You: {messages[-1]['content']}"}}]
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
    "gpt-35": gpt_35,
    "gpt-4": gpt_4,
    "gpt-4o": gpt_4o,
    "mock": MockModel(),
}


def get_model(model_name: str):
    model = models[model_name]
    return model
