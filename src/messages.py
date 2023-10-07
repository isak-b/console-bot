import os
import json
from colorama import Fore, Style

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"


def load_prompt(path: str, filename: str) -> dict:
    """Load prompt from file"""
    with open(ROOT_PATH + path + filename, "r") as f:
        content = f.read()
    return {"role": "system", "content": content}


def load_history(path: str, filename: str) -> list:
    """Load chat history from file"""
    result = []
    if os.path.exists(ROOT_PATH + path + filename) is True:
        with open(ROOT_PATH + path + filename, "r") as f:
            result = json.load(f)
    return result


def get_question(args: list) -> str:
    """Get question from args"""
    content = " ".join(args) if isinstance(args, list) else str(args)
    return {"role": "user", "content": content}


def get_msgs(prompt: dict, history: list, question: dict, history_size: int = 10) -> list:
    """Get messages for bot to respond to"""
    history = history[-history_size:] if history_size else history
    msgs = [prompt] + history + [question]
    return msgs


def get_answer(msgs: list, model, print_answer: bool = True) -> dict:
    """Get answer from bot"""
    answer = model(messages=msgs).choices[0]["message"]
    if print_answer is True:
        print(Fore.LIGHTBLUE_EX + "bot: " + answer["content"] + Style.RESET_ALL)
    return answer


def print_history(history: list, i: int = None) -> None:
    """Print chat history to console"""
    i = -1 * int(i) if i else -1
    try:
        msg = history[i]
    except IndexError:
        return print(f"No chat history to print: {len(history)=}")
    print(f"history[{i}]: {msg['content']}")


def save_msg(msg: str, path: str, filename: str = None) -> None:
    """Save message to file"""
    if not filename:
        files = os.listdir(ROOT_PATH + path)
        max_num = 0
        for file in files:
            if file.startswith("output_"):
                try:
                    num = int(file.split("_")[1].split(".")[0])
                except ValueError:
                    continue
                max_num = max(num, max_num)
        new_num = max_num + 1
        filename = f"output_{str(new_num).zfill(3)}.txt"

    output_path = f"{ROOT_PATH}{path}{filename}"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(msg)
    print(f"Output saved to {output_path=}")


def save_history(history: list, path: str, filename: str) -> None:
    """Save chat history to file"""
    if history:
        with open(ROOT_PATH + path + filename, "w") as f:
            json.dump(history, f)
