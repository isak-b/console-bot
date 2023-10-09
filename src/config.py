import os
import yaml
from colorama import Fore, Style

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/"
cfg_path = os.path.join(ROOT_PATH, "config.yaml")


def load_cfg(path: str = cfg_path) -> dict:
    """Load config from file"""
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)
    return cfg


def save_cfg(cfg: dict, path: str = cfg_path) -> None:
    """Save config to file"""
    with open(path, "w") as f:
        yaml.dump(cfg, f)


def print_cfg(cfg: dict, highlight_key: str = None) -> None:
    """Print config to console"""
    cfg_str = ""
    for line in yaml.dump(cfg, sort_keys=False).split("\n"):
        if highlight_key and line.startswith(highlight_key):
            cfg_str += f"{Fore.CYAN}{Style.BRIGHT}>> {line}{Style.RESET_ALL}\n"
        else:
            cfg_str += f"{Fore.LIGHTBLACK_EX}{line}{Style.RESET_ALL}\n"
    print(cfg_str)


def process_cfg_value(value: str) -> str | int | bool:
    """Process config value"""
    if value.lower() in ["true", "false"]:
        value = value.lower() == "true"
    elif value.isdigit():
        value = int(value)
    return value
