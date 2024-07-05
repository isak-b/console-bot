import os
import re
import yaml

APP_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_CFG_PATH = os.path.join(APP_PATH, "config.yaml")


def load_cfg(cfg_path: str = None, make_paths_absolute: bool = True) -> dict:
    """Load config from file"""
    cfg_path = cfg_path or DEFAULT_CFG_PATH
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)
    cfg["paths"]["config_dir"] = os.path.dirname(cfg_path)

    # Make paths absolute
    for dir_name, dir_path in cfg["paths"].items():
        if make_paths_absolute is True and dir_path.startswith("/") is False:
            cfg["paths"][dir_name] = os.path.join(cfg["paths"]["config_dir"], dir_path)

    return cfg


def save_cfg(cfg: dict, path: str = DEFAULT_CFG_PATH) -> None:
    """Save config to file"""
    with open(path, "w") as f:
        yaml.dump(cfg, f, sort_keys=False)


def load_bots(bots_path: str) -> dict:
    """Load bots from files"""
    bots = {}
    for filename in os.listdir(bots_path):
        file_path = os.path.join(bots_path, filename)
        with open(file_path, "r") as f:
            bots[filename.removesuffix(".txt")] = f.read()
    return bots


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
