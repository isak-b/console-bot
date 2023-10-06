import functools
import openai

gpt3_5_standard = functools.partial(
    openai.ChatCompletion.create,
    model="gpt-3.5-turbo",
)

default_model = gpt3_5_standard
