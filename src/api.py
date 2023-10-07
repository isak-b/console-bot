import os
import openai
from dotenv import load_dotenv

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


def set_api_key(model_name: str, env_filename: str) -> None:
    if model_name in ["default", "gpt3_5_standard"]:
        _load_openai_api_key(env_filename=env_filename)
