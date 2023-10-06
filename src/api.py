import os
import openai
from dotenv import load_dotenv
from typing import Callable

load_dotenv()
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"


def _load_openai_api_key(env_filename: str) -> None:
    """Load OpenAI API key from .env file"""
    path = ROOT_PATH + env_filename
    if os.path.exists(path) is False:
        raise FileNotFoundError(f"{path} file not found")
    if os.getenv("OPENAI_API_KEY") is None:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    # Set API key
    openai.api_key = os.getenv("OPENAI_API_KEY")


def set_api_key(env_filename: str, api_key_loader: Callable[[dict], None] = _load_openai_api_key) -> None:
    api_key_loader(env_filename=env_filename)
