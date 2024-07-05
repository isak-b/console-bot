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
DEFAULT_CONFIG_PATH = os.path.join(ROOT_PATH, "ask", "config.yaml")


def main(question: str, cfg_path: str = DEFAULT_CONFIG_PATH) -> str:
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
