import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
sys.path.insert(0, ROOT_PATH)

from chat.bot import ChatBot  # noqa: E402
from chat.utils import load_cfg, is_markdown

load_dotenv()


def main(question: str) -> str:
    """A simpler non-chat version of the ConsoleBot. Use it to ask a single question and print the answer to console.
    NOTE: Call `python console-bot/chat` to open the chat interface instead."""

    # Initialize bot
    cfg = load_cfg(os.path.join(ROOT_PATH, "ask", "config.yaml"))
    bot = ChatBot(cfg=cfg)

    # Get answer
    answer = bot.chat(question)
    if is_markdown(answer):
        answer = Markdown(answer)

    # Print to console
    console = Console()
    console.print(f"\[{bot.cfg['model']}]:", answer)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        question = input("Question: ")
    else:
        question = "".join(sys.argv[1:])
    main(question)
