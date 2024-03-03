import os
import yaml

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
        yaml.dump(cfg, f, sort_keys=False)


def get_formatted_cfg(cfg: dict, options: dict = None, highlight_keys: list = None):
    formatted_dict = "\n"
    for line in yaml.dump(cfg, default_flow_style=False, sort_keys=False).split("\n"):
        key = line.strip().split(":")[0]
        line += f" {options[key]}" if options is not None and key in options else ""
        if highlight_keys:
            if key in highlight_keys:
                line = f"<b><ansicyan>{line}</ansicyan></b>"
            else:
                line = f"<ansigray>{line}</ansigray>"
        formatted_dict += f"{line}\n"
    formatted_dict = formatted_dict.rstrip("\n")
    return formatted_dict
