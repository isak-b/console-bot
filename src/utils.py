import os
import re
import glob
import yaml
import json
from datetime import datetime


def load_cfg(cfg_path: str, make_paths_absolute: bool = True) -> dict:
    """Load config from file"""
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)
    cfg["paths"]["config_dir"] = os.path.dirname(cfg_path)

    # Make paths absolute
    for name, path in cfg["paths"].items():
        if make_paths_absolute is True and os.path.isabs(path) is False:
            cfg["paths"][name] = os.path.join(cfg["paths"]["config_dir"], path)

    return cfg


def save_cfg(cfg: dict, path: str) -> None:
    """Save config to file"""
    with open(path, "w") as f:
        yaml.dump(cfg, f, sort_keys=False)


def load_files(path: str, add_created_datetime: bool = False) -> dict:
    """Load files from a path and return as dict"""
    output = {}
    files = list(filter(os.path.isfile, glob.glob(path + "*")))
    if add_created_datetime is True:
        files.sort(key=lambda x: os.path.getctime(x), reverse=True)

    for file_path in files:
        name = os.path.splitext(os.path.basename(file_path))[0]
        content = None
        with open(os.path.join(path, file_path), "r") as f:
            if file_path.endswith(".txt"):
                content = f.read()
            elif file_path.endswith(".json"):
                content = json.load(f)
            elif file_path.endswith(".yaml"):
                content = yaml.safe_load(f)

        if content is not None:
            if add_created_datetime is True:
                output[name] = {"content": content, "date": datetime.fromtimestamp(os.path.getctime(file_path))}
            else:
                output[name] = content
    return output


def save_messages(messages: list, path: str) -> None:
    """Save messages to a file"""
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    with open(path, "w") as f:
        if path.endswith(".yaml"):
            yaml.dump(messages, f, sort_keys=False)
        elif path.endswith(".json"):
            json.dump(messages, f, indent=2)


def is_markdown(text: str) -> bool:
    """Check if text contains any markdown syntax"""
    markdown_patterns = [
        r"^\s*#{1,6}\s",  # Headers
        r"^\s*>\s",  # Blockquotes
        r"\[.*\]\(.*\)",  # Links
        r"\*\*.*\*\*",  # Bold text
        r"\*.*\*",  # Italic text
        r"`.*`",  # Inline code
        r"^\s*-{3,}\s*$",  # Horizontal rules
        r"^\s*\d+\.\s",  # Ordered lists
        r"^\s*[-*+]\s",  # Unordered lists
    ]
    for pattern in markdown_patterns:
        if re.search(pattern, text, re.MULTILINE):
            return True
    return False


def get_time_separator(event_date: datetime, current_date: datetime = datetime.now()):
    """Get time separator based on event_date vs. current_date"""
    days_diff = (current_date - event_date).days
    event_week = event_date.strftime("%W")
    event_month = event_date.strftime("%B")
    event_year = event_date.strftime("%Y")

    current_week = current_date.strftime("%W")
    current_month = current_date.strftime("%B")
    current_year = current_date.strftime("%Y")

    if days_diff < 1:
        separator = "Today"
    elif days_diff < 2:
        separator = "Yesterday"
    elif event_year == current_year and event_month == current_month and event_week == current_week:
        separator = "This week"
    elif event_year == current_year and event_month == current_month:
        separator = "This month"
    elif event_year == current_year:
        separator = event_month
    else:
        separator = event_year

    return separator
