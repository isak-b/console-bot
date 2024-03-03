import os
import json
from prompt_toolkit import prompt

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"


def load_instruction(path: str) -> dict:
    """Load instruction from file"""
    with open(ROOT_PATH + path, "r") as f:
        content = f.read()
    return {"role": "system", "content": content}


def load_history(path: str) -> list:
    """Load chat history from file"""
    result = []
    if os.path.exists(ROOT_PATH + path) is True:
        with open(ROOT_PATH + path, "r") as f:
            result = json.load(f)
    return result


def get_question(args: list) -> str:
    """Get question from args"""
    content = " ".join(args) if isinstance(args, list) else str(args)
    return {"role": "user", "content": content}


def get_msgs(instruction: dict, history: list, question: dict, history_size: int = 10) -> list:
    """Get messages for bot to respond to"""
    history = history[-history_size:] if history_size else history
    msgs = [instruction] + history + [question]
    return msgs


def get_answer(msgs: list, model) -> dict:
    """Get answer from bot"""
    return model(messages=msgs).choices[0]["message"]


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
    print(f">> saved message:\n  {msg=}\n  {output_path=}")


def save_history(history: list, path: str, filename: str) -> None:
    """Save chat history to file"""
    output_path = f"{ROOT_PATH}{path}{filename}"
    if history:
        with open(output_path, "w") as f:
            json.dump(history, f)
            print(f">> history saved: {output_path}")
    else:
        print(f">> no history to save, delete file manually if you want it removed: {output_path}")
