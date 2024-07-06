import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG_PATH = os.path.join(ROOT_PATH, "profiles/ask/config.yaml")
sys.path.insert(0, ROOT_PATH)

from src.bot import ChatBot
from src.utils import load_cfg, is_markdown

load_dotenv()


def main(question: str, cfg_path: str = None) -> str:
    """A simpler non-chat version of the ConsoleBot. Use it to ask a single question and print the answer to console.
    NOTE: Doesn't have a chat history, call `python console-bot/chat` full functionality.
    """

    # Initialize bot
    cfg_path = cfg_path or DEFAULT_CONFIG_PATH
    cfg = load_cfg(cfg_path=cfg_path)
    bot = ChatBot(cfg=cfg)

    # Get answer
    answer = bot.chat(question)
    if is_markdown(answer):
        answer = Markdown(answer)

    # Print to console
    console = Console()
    tags = Markdown(f"\[\033[34m{bot.cfg['bot']}\033[0m]\[\033[36m{bot.cfg['model']}\033[0m]:")
    console.print(tags, answer)


if __name__ == "__main__":
    cfg_path = None
    if len(sys.argv) == 1:
        question = input("Question: ")
    else:
        question = "".join(sys.argv[1:])
    if len(sys.argv) > 2:
        cfg_path = sys.argv[2]
    main(question=question, cfg_path=cfg_path)
